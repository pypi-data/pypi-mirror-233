#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from tqdm import tqdm
import logging
import matplotlib.pyplot as plt
import math
import torch
from torch.autograd import Variable
import os
import torch
from orcaz.train_utils import *
from orcaz.NiftiDataset import *
from orcaz.registration import *
from orcaz import image_processing, constants
import orcaz.NiftiDataset as NiftiDataset
import torch.optim as optim
import torch.nn as nn
from orcaz.generators import build_netG
from orcaz.options import Options
from orcaz import resources
from orcaz import settings

def from_numpy_to_itk(image_np, image_itk):
    image_np = np.transpose(image_np, (2, 1, 0))
    image = sitk.GetImageFromArray(image_np)
    image.SetOrigin(image_itk.GetOrigin())
    image.SetDirection(image_itk.GetDirection())
    image.SetSpacing(image_itk.GetSpacing())
    return image

def prepare_batch(image, ijk_patch_indices):
    image_batches = []
    for batch in ijk_patch_indices:
        image_batch = []
        for patch in batch:
            image_patch = image[patch[0]:patch[1],
                                patch[2]:patch[3], patch[4]:patch[5]]
            image_batch.append(image_patch)

        image_batch = np.asarray(image_batch)
        # image_batch = image_batch[:, :, :, :, np.newaxis]
        image_batches.append(image_batch)

    return image_batches


# inference single image
def inference(write_image, model, image_path, result_path, resolution, patch_size_x, patch_size_y, patch_size_z, stride_inplane, stride_layer, batch_size=1, Logger=True):
    #Get device to run the model
    device = resources.check_cuda(True)

    # Check if image requires resizing
    resample = False
    sitk_image = sitk.ReadImage(image_path)
    original_resolution =  sitk_image.GetSpacing()
    original_size = sitk_image.GetSize()
    if resolution != sitk_image.GetSpacing():
        resample = True
        logging.info("Resampling ...")

    # create transformations to image and labels
    transforms1 = [
        NiftiDataset.Resample(resolution, resample)
    ]

    transforms2 = [
        NiftiDataset.Padding((patch_size_x, patch_size_y, patch_size_z))
    ]

    # read image file
    reader = sitk.ImageFileReader()
    reader.SetFileName(image_path)
    image = reader.Execute()

    # normalize the image
    image = Normalization(image)

    castImageFilter = sitk.CastImageFilter()
    castImageFilter.SetOutputPixelType(sitk.sitkFloat32)
    image = castImageFilter.Execute(image)

    # create empty label in pair with transformed image
    label_tfm = sitk.Image(image.GetSize(), sitk.sitkFloat32)
    label_tfm.SetOrigin(image.GetOrigin())
    label_tfm.SetDirection(image.GetDirection())
    label_tfm.SetSpacing(image.GetSpacing())

    sample = {'image': image, 'label': label_tfm}

    for transform in transforms1:
        sample = transform(sample)

    # keeping track on how much padding will be performed before the inference
    image_array = sitk.GetArrayFromImage(sample['image'])
    pad_x = patch_size_x - (patch_size_x - image_array.shape[2])
    pad_y = patch_size_x - (patch_size_y - image_array.shape[1])
    pad_z = patch_size_z - (patch_size_z - image_array.shape[0])

    image_pre_pad = sample['image']

    for transform in transforms2:
        sample = transform(sample)

    image_tfm, label_tfm = sample['image'], sample['label']

    # convert image to numpy array
    image_np = sitk.GetArrayFromImage(image_tfm)
    label_np = sitk.GetArrayFromImage(label_tfm)

    label_np = np.asarray(label_np, np.float32)

    # unify numpy and sitk orientation
    image_np = np.transpose(image_np, (2, 1, 0))
    label_np = np.transpose(label_np, (2, 1, 0))

    # ----------------- Padding the image if the z dimension still is not even ----------------------

    if (image_np.shape[2] % 2) == 0:
        Padding = False
    else:
        image_np = np.pad(image_np, ((0, 0), (0, 0), (0, 1)), 'edge')
        label_np = np.pad(label_np, ((0, 0), (0, 0), (0, 1)), 'edge')
        Padding = True

    # ------------------------------------------------------------------------------------------------

    # if Weighting option is set for stiching the patches
    
    gaussian_weighting = True
    if gaussian_weighting:
        sigma_scale = [.2, .2, .2]
        patch_size = [patch_size_x, patch_size_y, patch_size_z]
        sigmas = [i * sigma_s for i, sigma_s in zip(patch_size, sigma_scale)]
        importance_map = torch.ones(
            patch_size, device=device, dtype=torch.float)
        for i in range(len(patch_size)):
            x = torch.arange(
                start=-(patch_size[i] - 1) / 2.0, end=(patch_size[i] - 1) / 2.0 + 1, dtype=torch.float, device=device
            )
            x = torch.exp(x**2 / (-2 * sigmas[i] ** 2))  # 1D gaussian
            importance_map = importance_map.unsqueeze(
                -1) * x[(None,) * i] if i > 0 else x

        min_non_zero = max(torch.min(importance_map).item(), 1e-3)
        importance_map = torch.clamp_(importance_map.to(
            torch.float), min=min_non_zero).to(torch.float32)

    logging.info("Preparing patches for prediction ...")

    # a weighting matrix will be used for averaging the overlapped region
    weight_np = np.zeros(label_np.shape)

    # prepare image batch indices
    inum = int(
        math.ceil((image_np.shape[0] - patch_size_x) / float(stride_inplane))) + 1
    jnum = int(
        math.ceil((image_np.shape[1] - patch_size_y) / float(stride_inplane))) + 1
    knum = int(
        math.ceil((image_np.shape[2] - patch_size_z) / float(stride_layer))) + 1

    patch_total = 0
    ijk_patch_indices = []
    ijk_patch_indicies_tmp = []

    for i in range(inum):
        for j in range(jnum):
            for k in range(knum):
                if patch_total % batch_size == 0:
                    ijk_patch_indicies_tmp = []

                istart = i * stride_inplane
                if istart + patch_size_x > image_np.shape[0]:  # for last patch
                    istart = image_np.shape[0] - patch_size_x
                iend = istart + patch_size_x

                jstart = j * stride_inplane
                if jstart + patch_size_y > image_np.shape[1]:  # for last patch
                    jstart = image_np.shape[1] - patch_size_y
                jend = jstart + patch_size_y

                kstart = k * stride_layer
                if kstart + patch_size_z > image_np.shape[2]:  # for last patch
                    kstart = image_np.shape[2] - patch_size_z
                kend = kstart + patch_size_z

                ijk_patch_indicies_tmp.append(
                    [istart, iend, jstart, jend, kstart, kend])

                if patch_total % batch_size == 0:
                    ijk_patch_indices.append(ijk_patch_indicies_tmp)

                patch_total += 1

    batches = prepare_batch(image_np, ijk_patch_indices)

    logging.info("Running prediction ...")
    if Logger is True:

        for i in range(len(batches)):
            batch = batches[i]

            batch = (batch - 127.5) / 127.5

            batch = torch.from_numpy(batch[np.newaxis, :, :, :])
            if device=="cuda":
                batch = Variable(batch.cuda())
            else:
                batch = Variable(batch.cpu())


            pred = model(batch)
            pred = pred.squeeze().data.cpu().numpy()

            pred = (pred * 127.5) + 127.5

            istart = ijk_patch_indices[i][0][0]
            iend = ijk_patch_indices[i][0][1]
            jstart = ijk_patch_indices[i][0][2]
            jend = ijk_patch_indices[i][0][3]
            kstart = ijk_patch_indices[i][0][4]
            kend = ijk_patch_indices[i][0][5]
            label_np[istart:iend, jstart:jend, kstart:kend] += pred[:, :, :] * \
                importance_map.cpu().numpy(
            ) if gaussian_weighting else pred[:, :, :]
            weight_np[istart:iend, jstart:jend,
                      kstart:kend] += importance_map.cpu().numpy() if gaussian_weighting else 1
    else:

        for i in tqdm(range(len(batches))):
            batch = batches[i]

            batch = (batch - 127.5) / 127.5

            batch = torch.from_numpy(batch[np.newaxis, :, :, :])
            if device=="cuda":
                batch = Variable(batch.cuda())
            else:
                batch = Variable(batch.cpu())

            pred = model(batch)
            pred = pred.squeeze().data.cpu().numpy()

            pred = (pred * 127.5) + 127.5

            istart = ijk_patch_indices[i][0][0]
            iend = ijk_patch_indices[i][0][1]
            jstart = ijk_patch_indices[i][0][2]
            jend = ijk_patch_indices[i][0][3]
            kstart = ijk_patch_indices[i][0][4]
            kend = ijk_patch_indices[i][0][5]
            label_np[istart:iend, jstart:jend, kstart:kend] += pred[:, :, :] * \
                importance_map.cpu().numpy(
            ) if gaussian_weighting else pred[:, :, :]
            weight_np[istart:iend, jstart:jend,
                      kstart:kend] += importance_map.cpu().numpy() if gaussian_weighting else 1

        logging.info("Prediction complete.")

    # eliminate overlapping region using the weighted value
    label_np = (np.float32(label_np) / np.float32(weight_np) + 0.01)

    # removed the 1 pad on z
    if Padding is True:
        label_np = label_np[:, :, 0:(label_np.shape[2]-1)]

    # removed all the padding
    label_np = label_np[:pad_x, :pad_y, :pad_z]

    # convert back to sitk space
    label = from_numpy_to_itk(label_np, image_pre_pad)
    # ---------------------------------------------------------------------------------------------

    # save label
    writer = sitk.ImageFileWriter()

    if resample is True:
        logging.info("Resampling label back to original image space...")
        label = resample_sitk_image_exact_dimension(
            label, new_spacing=original_resolution,new_size=original_size, interpolator='bspline')
    else:
        label = label
    
    logging.info("Output resolution is "+str(label.GetSize()))

    writer.SetFileName(result_path)
    if write_image is True:
        writer.Execute(label)
        logging.info("Save evaluate label at {} success".format(result_path))
        return label
    else:
        return label

def predict(opt: Options, orca_dir: str, ct_dir: str, pt_dir: str) -> None:

    if resources.check_cuda()=="cuda":
        net = build_netG(opt).cuda()  # load the network Unet
    else:
        net = build_netG(opt)

    net.load_state_dict(new_state_dict(settings.model_path))

    pt_file = glob.glob(os.path.join(pt_dir, '*PET*.nii*'))[0]
    _ = inference(write_image=True,
                  model=net,
                  image_path=pt_file, 
                  result_path=os.path.join(ct_dir, 'synth_ct_img.nii'),
                  resolution=opt.new_resolution,
                  patch_size_x=opt.patch_size[0],
                  patch_size_y=opt.patch_size[1],
                  patch_size_z=opt.patch_size[2],
                  stride_inplane=opt.stride_inplane,
                  stride_layer=opt.stride_layer,
                  Logger=False)

# TODO: To be writen seperately in another file, using the registration Functions from the ENHANCE framework
def motion_match(opt):

    import nibabel
    from scipy.ndimage import binary_dilation

    registrator = image_processing.ImageRegistration(opt.pet, constants.MULTI_RESOLUTION_SCHEME)

    # Load image and mask 
    movingimg = Path(opt.ct)
    ct_nib  = nibabel.load(movingimg.absolute())
    mask_img= nibabel.load(Path(opt.mask).absolute()).get_fdata()
    ct_img  = ct_nib.get_fdata()
    header_info = ct_nib.header

    mask_img = binary_dilation(mask_img, iterations=2)
    minimum = np.median(ct_img[~mask_img])
    ct_img[~mask_img]=minimum

    movingimg = movingimg.parent.absolute() / ("masked_"+movingimg.name)
    img = nibabel.Nifti1Image(ct_img, ct_nib.affine,header_info)
    print("Saving to "+ str(movingimg))
    nibabel.save(img, str(movingimg))

    home_dir = movingimg.parent
    print("Home dir "+str(home_dir))
    tmp_dir = home_dir / Path(opt.dout).name
    tmp_dir.mkdir(parents=True, exist_ok=True)

    mask_img_file = tmp_dir / "mask.nii"
    img = nibabel.Nifti1Image(mask_img, ct_nib.affine,header_info)
    print("Saving to "+str(mask_img_file))
    nibabel.save(img, str(mask_img_file))

    #Create and Save a dilated mask
    dil_mask = binary_dilation(mask_img, iterations=8)
    dil_mask = dil_mask.astype(np.float32)
    
    dmask_img = tmp_dir / "dill_mask.nii"
    mimg = nibabel.Nifti1Image(dil_mask, ct_nib.affine,header_info)
    print("Saving to "+str(dmask_img))
    nibabel.save(mimg, str(dmask_img))
    
    # Saving the filetered image
    flt_img = tmp_dir / str("filetered_"+movingimg.name)
    filter(movingimg, str(flt_img))

    if (opt.gpu_id != -1) & torch.cuda.is_available():
        # device = torch.device("cuda:0")
        os.environ["CUDA_VISIBLE_DEVICES"] = opt.gpu_id
        net = build_netG(opt).cuda()  # load the network Unet
    else:
        net = build_netG(opt)

    net.load_state_dict(new_state_dict(opt.weights))


    tmp_dir = flt_img.parent
    synth_ct_img = tmp_dir / "synth_ct_img.nii"

    _ = inference(write_image=True,
                  model=net,
                  image_path=opt.pet,
                  result_path=str(synth_ct_img),
                  resolution=opt.new_resolution,
                  patch_size_x=opt.patch_size[0],
                  patch_size_y=opt.patch_size[1],
                  patch_size_z=opt.patch_size[2],
                  stride_inplane=opt.stride_inplane,
                  stride_layer=opt.stride_layer,
                  Logger=False)

    affine(fixed_img=str(synth_ct_img),
           moving_img=movingimg,
           registration_sequence="initial",
           directory=str(tmp_dir),
           cost_function="NCC 2x2x2",
           multi_resolution_iterations="100x50x10",
           nb_threads=opt.workers
           )

    deformable(fixed_img=str(synth_ct_img),
               moving_img=str(flt_img),
               registration_sequence="",
               directory=str(tmp_dir),
               cost_function="NCC 2x2x2",
               multi_resolution_iterations="100x50x10",
               nb_threads=opt.workers,
               mask_img=str(dmask_img)
               )
    # Mask directly the warp file; not used since it reduces the overall effecto  the transformation within the body as well.
    # warp_file =  tmp_dir / str("_warp.nii.gz")
    # warp_nib = nibabel.load(str(warp_file))
    # warp_img = warp_nib.get_fdata()
    # mask = np.bool_(mask_img)
    # warp_img[~mask]=0
    # img = nibabel.Nifti1Image(warp_img, warp_nib.affine,header_info)
    # nibabel.save(img,str(warp_file))
                       
    
    #resampled_img = tmp_dir / str("ORCA_Resampled_"+opt.movingimg)
    resampled_img = tmp_dir / ("ORCA_Resampled_"+str(Path(opt.ct).name))
    resample(fixed_img=str(synth_ct_img),
             moving_img=opt.ct,
             registration_sequence="",
             directory=str(tmp_dir),
             registration_type="deformable",
             resampled_img=str(resampled_img)
             )
