#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------------------------------------------------
# File: image_processing.py
# Project: Optimized Registration through Conditional Adversarial networks (ORCA)
# Author: Zacharias Chalampalakis | Lalith Kumar Shiyam Sundar | Sebastian Gutschmayer
# Institution: Medical University of Vienna
# Research Group: Quantitative Imaging and Medical Physics (QIMP) Team
# Date: 19.07.2023
# Version: 0.1.0
#
# Description:
# This module handles image processing for orca.
#
# Usage:
# The functions in this module can be imported and used in other modules within orca to perform image conversion.
# ----------------------------------------------------------------------------------------------------------------------

import SimpleITK as sitk
import contextlib
import time
import glob
from orcaz import constants
from orcaz.constants import FALCON_PATH
from orcaz.file_utilities import *
from mpire import WorkerPool
import multiprocessing
from rich.progress import Progress
from concurrent.futures import ThreadPoolExecutor
from moosez import moose
import os
import nibabel as nib
import numpy as np
import pathlib
import subprocess
import logging
import sys
import re
from orcaz import resources
from rich.progress import track
import nibabel
from scipy.ndimage import binary_dilation
from nifti2dicom.converter import save_dicom_from_nifti_image

DEBUG_MODE=False


def process_and_moose_ct_files(ct_dir: str, mask_dir: str, moose_model: str, accelerator: str):
    # Get the ct_files in the ct_dir that are resampled to the PET space
    ct_files = get_files(ct_dir, 'resampled*.nii*')

    with Progress() as progress_bar:
        task = progress_bar.add_task("[cyan] MOOSE-ing CT files...", total=len(ct_files))

        for ct_file in ct_files:
            base_name = os.path.basename(ct_file).split('.')[0]

            ct_file_dir = os.path.join(ct_dir, base_name)
            create_directory(ct_file_dir)
            move_file(ct_file, os.path.join(ct_file_dir, os.path.basename(ct_file)))

            mask_file_dir = os.path.join(mask_dir, base_name)
            create_directory(mask_file_dir)

            progress_bar.update(task, advance=0, description=f"[cyan] Running MOOSE on {base_name}...")

            with open(os.devnull, 'w') as devnull:
                with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
                    moose(moose_model, ct_file_dir, mask_file_dir, accelerator)

            progress_bar.update(task, advance=0, description=f"[cyan] Completed MOOSE on {base_name}, cleaning up...")

            move_files_to_directory(ct_file_dir, ct_dir)
            move_files_to_directory(mask_file_dir, mask_dir)

            remove_directory(ct_file_dir)
            remove_directory(mask_file_dir)

            progress_bar.update(task, advance=1, description=f"[cyan] Finished processing {base_name}")

            time.sleep(1)  # delay for 1 second

def change_mask_labels(mask_file: str, label_map: dict, excluded_labels: list):
    # Load the image
    img = nib.load(mask_file)

    # Get the image data (returns a numpy array)
    data = img.get_fdata()

    # Prepare labels for modification
    excluded_indices = [idx for idx, lbl in label_map.items() if lbl in excluded_labels]
    other_indices = [idx for idx, lbl in label_map.items() if lbl not in excluded_labels]

    # Set the labels
    data[np.isin(data, excluded_indices)] = 0
    data[np.isin(data, other_indices)] = 1

    # Save the modified image
    new_img = nib.Nifti1Image(data, img.affine, img.header)
    nib.save(new_img, mask_file)

def reslice_identity(reference_image: sitk.Image, moving_image: sitk.Image, 
                     output_image_path: str = None, is_label_image: bool = False, median=-1024) -> sitk.Image:
    """
    Reslice an image to the same space as another image
    :param reference_image: The reference image
    :param moving_image: The image to reslice to the reference image
    :param output_image_path: Path to the resliced image
    :param is_label_image: Determines if the image is a label image. Default is False
    """
    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(reference_image)
    resampler.SetDefaultPixelValue(int(median))

    if is_label_image:
        resampler.SetInterpolator(sitk.sitkNearestNeighbor)
    else:
        resampler.SetInterpolator(sitk.sitkBSpline)

    resampled_image = resampler.Execute(moving_image)
    resampled_image = sitk.Cast(resampled_image, sitk.sitkInt32)
    if output_image_path is not None:
        sitk.WriteImage(resampled_image, output_image_path)
    return resampled_image


def prepare_reslice_tasks(subject_directory: str):
    tasks = []
    ct_file = glob.glob(os.path.join(subject_directory, '*CT*.nii*'))
    pt_file = glob.glob(os.path.join(subject_directory, '*PET*.nii*'))
    resliced_ct_file = os.path.join(subject_directory, constants.RESAMPLED_PREFIX + '_' +
                                    os.path.basename(ct_file[0]))

    tasks.append((
        sitk.ReadImage(pt_file[0]),
        sitk.ReadImage(ct_file[0]),
        resliced_ct_file,
        False
    ))
    return tasks


def copy_and_rename_file(src, dst, subdir):
    copy_file(src, dst)
    new_file = os.path.join(dst, os.path.basename(subdir) + '_' + os.path.basename(src))
    os.rename(os.path.join(dst, os.path.basename(src)), new_file)


def preprocess(subject_dir: str, num_workers: int = None):
    """
    Preprocesses the images in the subject directory
    :param puma_compliant_subjects: The puma compliant subjects
    :param num_workers: The number of worker processes for parallel processing
    """
    if num_workers is None:
        num_workers = multiprocessing.cpu_count()

    tasks = prepare_reslice_tasks(subject_dir)

    #Process tasks in parallel using mpire
    with WorkerPool(n_jobs=num_workers) as pool:
        with Progress() as progress:
            task = progress.add_task("[cyan] Preprocessing ORCA compliant subjects ", total=len(tasks))

            for _ in pool.map(reslice_identity, tasks):
                progress.update(task, advance=1)

    # set puma working directory
 
    orca_working_dir = os.path.join(os.path.abspath(subject_dir), constants.ORCA_WORKING_FOLDER)
    create_directory(orca_working_dir)

    # create CT and PET folders
    ct_dir = os.path.join(orca_working_dir, constants.MODALITIES[1])
    pt_dir = os.path.join(orca_working_dir, constants.MODALITIES[0])
    mask_dir = os.path.join(orca_working_dir, constants.MASK_FOLDER)
    create_directory(ct_dir)
    create_directory(pt_dir)


    # Move and rename files
    ct_files = glob.glob(os.path.join(subject_dir, '*CT*.nii*'))
    for ct_file in ct_files: move_file(ct_file, ct_dir)
    pt_files = glob.glob(os.path.join(subject_dir, '*PET*.nii*'))
    for pt_file in pt_files: move_file(pt_file, pt_dir)

    # Run moosez to get the masks
    process_and_moose_ct_files(ct_dir, mask_dir, constants.MOOSE_MODEL, constants.ACCELERATOR)

    # remove the prefix from the mask files
    for mask_file in glob.glob(os.path.join(mask_dir, constants.MOOSE_PREFIX + '*')):
        new_mask_file = re.sub(rf'{constants.MOOSE_PREFIX}', '', mask_file)
        os.rename(mask_file, new_mask_file)
        # for ORCA the whole body contour is needed, so no masks are removed. 
        #change_mask_labels(new_mask_file, constants.MOOSE_LABEL_INDEX, ["Arms"])

    # process the mask files for ORCA
    process_mask(mask_dir)

    return orca_working_dir, ct_dir, pt_dir, mask_dir

def postprocess(orca_working_dir: str, ct_dir: int = None, mask_dir: int = None):
    ct_file = glob.glob(os.path.join(ct_dir, 'CT_img.nii*'))[0]
    resampled_moving_img = glob.glob(os.path.join(orca_working_dir, constants.ALIGNED_CT_FOLDER + "/ORCA*.nii*"))[0]
    _ = reslice_identity(sitk.ReadImage(ct_file), sitk.ReadImage(resampled_moving_img),
                        os.path.join(orca_working_dir, constants.ALIGNED_CT_FOLDER + "/ORCA_aligned_CT.nii.gz"),
                        is_label_image=False)
    
    resampled_moving_mask = glob.glob(os.path.join(mask_dir, "ORCA*.nii*"))[0]
    _ = reslice_identity(sitk.ReadImage(ct_file), sitk.ReadImage(resampled_moving_mask),
                        os.path.join(os.path.abspath(mask_dir), "ORCA_aligned_mask.nii.gz"),
                        is_label_image=True, median=0)
    
    # Clean up the edges of the CT images 
    for ct_file in glob.glob(os.path.join(orca_working_dir, constants.ALIGNED_CT_FOLDER + "/*.nii*")): 
        #ToDo Make this search better, filenaming is not consistent
        mask_file = "ORCA_aligned_resampled_toPET_CT.nii.gz" if ct_file.endswith("0000.nii.gz") else "ORCA_aligned_mask.nii.gz"
        mask_CT_edges(ct_file, os.path.join(mask_dir, mask_file),edge_trim=50,top_trim=10)
    
    # Clip CT values lower than -1024 to -1024
    for ct_file in glob.glob(os.path.join(orca_working_dir, constants.ALIGNED_CT_FOLDER + "/*.nii*")):   
        ct_image = nibabel.load(ct_file)
        ct_image_data = ct_image.get_fdata()
        ct_image_data[ct_image_data < -1024] = -1024
        nibabel.save(nibabel.Nifti1Image(ct_image_data, ct_image.affine), ct_file)


class ImageRegistration:
    def __init__(self, fixed_img: str, multi_resolution_iterations: str, num_workers: int, fixed_mask: str = None):
        self.fixed_img = fixed_img
        self.fixed_mask = fixed_mask
        self.multi_resolution_iterations = multi_resolution_iterations
        self.num_workers = num_workers
        self.moving_img = None
        self.transform_files = None

    def set_moving_image(self, moving_img: str, update_transforms: bool = True):
        self.moving_img = moving_img
        if update_transforms:
            out_dir = pathlib.Path(self.moving_img).parent
            moving_img_filename = pathlib.Path(self.moving_img).name
            self.transform_files = {
                'rigid': os.path.join(out_dir, f"{moving_img_filename}_rigid.mat"),
                'affine': os.path.join(out_dir, f"{moving_img_filename}_affine.mat"),
                'warp': os.path.join(out_dir, f"{moving_img_filename}_warp.nii.gz"),
                'inverse_warp': os.path.join(out_dir, f"{moving_img_filename}_inverse_warp.nii.gz")
            }

    def create_and_set_masked_moving_image(self, mask: str) -> float:
        """ Creates a masked moving image using the given mask
        :param mask: The mask to use
        """
        mask = nibabel.load(mask).get_fdata().astype(bool)
        print("self.moving image is ", self.moving_img, "\n") if DEBUG_MODE else None
        moving_image = nibabel.load(self.moving_img).get_fdata()
        # Set the background to the median value outside the mask
        median = np.median(moving_image[~mask])
        moving_image[~mask] = median
        nibabel.save(nibabel.Nifti1Image(moving_image, nibabel.load(self.moving_img).affine), \
                                    os.path.join(os.path.dirname(self.moving_img), 'masked_' + os.path.basename(self.moving_img)))
        self.masked_moving_image = os.path.join(os.path.dirname(self.moving_img), 'masked_' + os.path.basename(self.moving_img))
        print("self.masked_moving_image is ", self.masked_moving_image, "\n") if DEBUG_MODE else None
        return median 

    def rigid(self) -> str:
        mask_cmd = f"-gm {re.escape(self.fixed_mask)}" if self.fixed_mask else ""
        cmd_to_run = f"{FALCON_PATH} -d 3 -a -i {re.escape(self.fixed_img)} {re.escape(self.masked_moving_image)} " \
                     f"{mask_cmd} -ia-image-centers -dof 6 -o {re.escape(self.transform_files['rigid'])} " \
                     f"-n {self.multi_resolution_iterations} -m NCC 2x2x2 -threads {self.num_workers}"
        print("Rigid: cmd_to_run is ", cmd_to_run, "\n") if DEBUG_MODE else None
        subprocess.run(cmd_to_run, shell=True, capture_output=True)
        logging.info(
            f"Rigid alignment: {pathlib.Path(self.masked_moving_image).name} -> {pathlib.Path(self.fixed_img).name} | Aligned image: "
            f"moco-{pathlib.Path(self.masked_moving_image).name} | Transform file: {pathlib.Path(self.transform_files['rigid']).name}")
        return self.transform_files['rigid']

    def affine(self) -> str:
        mask_cmd = f"-gm {re.escape(self.fixed_mask)}" if self.fixed_mask else ""
        cmd_to_run = f"{FALCON_PATH} -d 3 -a -i {re.escape(self.fixed_img)} {re.escape(self.masked_moving_image)} " \
                     f"{mask_cmd} -ia-image-centers -dof 12 -o {re.escape(self.transform_files['affine'])} " \
                     f"-n {self.multi_resolution_iterations} -m NCC 2x2x2 -m NCC 2x2x2 -threads {self.num_workers}"
        subprocess.run(cmd_to_run, shell=True, capture_output=True)
        logging.info(
            f"Affine alignment: {pathlib.Path(self.masked_moving_image).name} -> {pathlib.Path(self.fixed_img).name} |"
            f" Aligned image: moco-{pathlib.Path(self.masked_moving_image).name} | Transform file: {pathlib.Path(self.transform_files['affine']).name}")
        return self.transform_files['affine']

    def deformable(self) -> tuple:
        self.rigid()
        mask_cmd = f"-gm {re.escape(self.fixed_mask)}" if self.fixed_mask else ""
        cmd_to_run = f"{FALCON_PATH} -d 3 -m NCC 2x2x2 -i {re.escape(self.fixed_img)} {re.escape(self.masked_moving_image)} " \
                     f"{mask_cmd} -it {re.escape(self.transform_files['rigid'])} -o {re.escape(self.transform_files['warp'])} " \
                     f"-n {self.multi_resolution_iterations} " \
                     f"-threads {self.num_workers}"
        print("Deformable: cmd_to_run is ", cmd_to_run, "\n") if DEBUG_MODE else None
        subprocess.run(cmd_to_run, shell=True, capture_output=True)
        logging.info(
            f"Deformable alignment: {pathlib.Path(self.masked_moving_image).name} -> {pathlib.Path(self.fixed_img).name} | "
            f"Aligned image: moco-{pathlib.Path(self.masked_moving_image).name} | "
            f"Initial alignment:{pathlib.Path(self.transform_files['rigid']).name}"
            f" | warp file: {pathlib.Path(self.transform_files['warp']).name}")
        return self.transform_files['rigid'], self.transform_files['warp'], self.transform_files['inverse_warp']

    def registration(self, registration_type: str) -> None:
        if registration_type == 'rigid':
            self.rigid()
        elif registration_type == 'affine':
            self.affine()
        elif registration_type == 'deformable':
            self.deformable()
        else:
            sys.exit("Registration type not supported!")

    def resample(self, resampled_moving_img: str, registration_type: str, median=0.0, 
                 segmentation="", resampled_seg="") -> None:
        if registration_type == 'rigid':
            cmd_to_run = self._build_cmd(resampled_moving_img, segmentation, resampled_seg,
                                         self.transform_files['rigid'], median=median)
        elif registration_type == 'affine':
            cmd_to_run = self._build_cmd(resampled_moving_img, segmentation, resampled_seg,
                                         self.transform_files['affine'], median=median)
        elif registration_type == 'deformable':
            cmd_to_run = self._build_cmd(resampled_moving_img, segmentation, resampled_seg,
                                         self.transform_files['warp'], self.transform_files['rigid'], 
                                         median=median)
        print("Resample: cmd_to_run is ", cmd_to_run, "\n") if DEBUG_MODE else None
        subprocess.run(cmd_to_run, shell=True, capture_output=True)

    def _build_cmd(self, resampled_moving_img: str, segmentation: str, resampled_seg: str,
                   *transform_files: str, median: float) -> str:
        cmd = f"{FALCON_PATH} -d 3 -rf {re.escape(self.fixed_img)} -ri LINEAR -rm " \
              f"{re.escape(self.moving_img)} {re.escape(resampled_moving_img)}"
        if segmentation and resampled_seg:
            cmd += f" -ri LABEL 0.2vox -rm {re.escape(segmentation)} {re.escape(resampled_seg)}"
        for transform_file in transform_files:
            cmd += f" -r {re.escape(transform_file)} -bg {median}"
        return cmd

def mask_CT_edges(ct_image: str, mask_file: str, edge_trim=10, top_trim=10) -> None:
    ct_image_nib = nibabel.load(ct_image)
    ct_image_data = ct_image_nib.get_fdata()
    mask = nibabel.load(mask_file).get_fdata()
    mask=mask.astype(bool)
    median = np.median(ct_image_data[~mask])

    for i in range(1,edge_trim):
        if (np.max(mask[:i,:,:])+np.max(mask[-i:,:,:])+np.max(mask[:,:i,:])+np.max(mask[:,-i:,:]))==0:
            ct_image_data[:i,:,:]=median
            ct_image_data[-i:,:,:]=median

            ct_image_data[:,:i,:]=median
            ct_image_data[:,-i:,:]=median
        else:
            break

    for i in range(1,top_trim):
        ct_image_data[:,:,-i][~mask[:,:,-i]]=median
        ct_image_data[:,:,i-1][~mask[:,:,i]]=median
    nibabel.save(nibabel.Nifti1Image(ct_image_data, ct_image_nib.affine), ct_image)


# def mask_CT(ct_dir: str, mask_dir: str, mask_id: str) -> None:
#     """
#     Masks the CT images in the ct_dir using the mask with the given identity
#     :param ct_dir: The directory containing the CT images
#     :param mask_dir: The directory containing the masks
#     :param mask_id: The identity of the mask to use
#     """
#     ct_files = sorted(glob.glob(os.path.join(ct_dir, 'resampled*.nii')))
#     mask =  glob.glob(os.path.join(mask_dir, f'{mask_id}*.nii*'))[0]
#     with Progress() as progress:
#         task = progress.add_task("[cyan] Masking CT files...", total=len(ct_files))

#         for ct_file in ct_files:
#             ct_image = nibabel.load(ct_file)
#             mask_image = nibabel.load(mask)
#             masked_image = nibabel.Nifti1Image(ct_image.get_fdata() * mask_image.get_fdata(), ct_image.affine)
#             nibabel.save(masked_image, os.path.join(ct_dir, f'{mask_id}_masked_' + os.path.basename(ct_file)))
#             progress.update(task, advance=1)

def get_mask(mask_dir: str, mask_id: str) -> str:
    """
    Gets the mask with the given identity
    :param mask_dir: The directory containing the masks
    :param mask_id: The identity of the mask to use
    :return: The path to the mask
    """
    return glob.glob(os.path.join(mask_dir, f'{mask_id}*.nii*'))[0]

def align(puma_working_dir: str, ct_dir: str, pt_dir: str, mask_dir: str, n_threads: int) -> None:
    reference_sCT_image = glob.glob(os.path.join(ct_dir, 'synth*.nii*'))[0]
    print("Using refference image of sCT: ", reference_sCT_image, "\n") if DEBUG_MODE else None
    moving_CT_image = glob.glob(os.path.join(ct_dir, 'resampled*.nii*'))[0]
    print("Using moving image of CT: ", moving_CT_image, "\n") if DEBUG_MODE else None
    mask = get_mask(mask_dir, 'dil8')

    with Progress() as progress:
        task = progress.add_task("[cyan] Aligning CT image to sCT", total=2)

        aligner = ImageRegistration(fixed_img=reference_sCT_image,
                                    multi_resolution_iterations=constants.MULTI_RESOLUTION_SCHEME,
                                    fixed_mask=mask, num_workers=n_threads)
        aligner.set_moving_image(moving_CT_image)
        median = aligner.create_and_set_masked_moving_image(get_mask(mask_dir, 'dil2'))
        aligner.registration('deformable')
        progress.update(task, advance=1)
        aligner.resample(resampled_moving_img=os.path.join(puma_working_dir, constants.ALIGNED_PREFIX +
                                                            os.path.basename(moving_CT_image)),
                            median=median, registration_type='deformable')
        
        # resample the mask to the new co-registered CT image
        aligner.resample(resampled_moving_img=os.path.join(puma_working_dir, constants.ALIGNED_PREFIX +
                                                            os.path.basename(moving_CT_image)),
                                                            segmentation=get_mask(mask_dir, 'resampled_'),
                                                            resampled_seg=os.path.join(mask_dir, constants.ALIGNED_PREFIX +
                                                            'resampled_toPET_CT.nii.gz'), median=median,
                            registration_type='deformable')
        
        # Clean up the edges of the resampled image
        # resampled_moving_img=os.path.join(puma_working_dir, constants.ALIGNED_PREFIX + os.path.basename(moving_CT_image))
        # ct_image = nibabel.load(resampled_moving_img)
        # ct_image_data = ct_image.get_fdata()
        # mask_file = os.path.join(mask_dir, constants.ALIGNED_PREFIX +'resampled_toPET_CT.nii.gz')
        # mask = nibabel.load(mask_file).get_fdata()
        # mask=mask.astype(bool)
        # median = np.median(ct_image_data[~mask])

        # for i in range(1,10):
        #     if (np.max(mask[:i,:,:])+np.max(mask[-i:,:,:])+np.max(mask[:,:i,:])+np.max(mask[:,-i:,:]))==0:
        #         ct_image_data[:i,:,:]=median
        #         ct_image_data[-i:,:,:]=median

        #         ct_image_data[:,:i,:]=median
        #         ct_image_data[:,-i:,:]=median
        #     else:
        #         break

        # for i in range(1,10):
        #     ct_image_data[:,:,-i][~mask[:,:,-i]]=median
        #     ct_image_data[:,:,i][~mask[:,:,i]]=median
        # nibabel.save(nibabel.Nifti1Image(ct_image_data, ct_image.affine), resampled_moving_img)

        
        progress.update(task, advance=1)


        # clean up transforms to a new folder
        rigid_transform_files = sorted(glob.glob(os.path.join(ct_dir, '*_rigid.mat')))
        warp_files = sorted(glob.glob(os.path.join(ct_dir, '*warp.nii.gz')))
        transforms_dir = os.path.join(puma_working_dir, constants.TRANSFORMS_FOLDER)
        create_directory(transforms_dir)
        # move all the warp files and rigid transform files to the transforms folder without zipping
        for rigid_transform_file in rigid_transform_files:
            move_file(rigid_transform_file, transforms_dir)
        for warp_file in warp_files:
            move_file(warp_file, transforms_dir)

        # move the aligned files to a new folder called aligned_CT, this is stored in the puma_working_dir
        aligned_ct_dir = os.path.join(puma_working_dir, constants.ALIGNED_CT_FOLDER)
        create_directory(aligned_ct_dir)
        # get aligned ct files using glob by looking for keyword 'aligned'
        aligned_ct_files = sorted(glob.glob(os.path.join(puma_working_dir, constants.ALIGNED_PREFIX + '*CT*.nii*')))
        for aligned_ct_file in aligned_ct_files:
            move_file(aligned_ct_file, aligned_ct_dir)

def export_dicom(puma_working_dir: str, ct_dir: str) -> None:
    print("Exporting to dicom \n") if DEBUG_MODE else None
    save_dicom_from_nifti_image(ref_dir=os.path.join(os.path.dirname(os.path.abspath(puma_working_dir)),"CT"),
                                nifti_path=glob.glob(os.path.join(puma_working_dir, constants.ALIGNED_CT_FOLDER, 'ORCA_aligned_CT.nii*'))[0],
                                output_dir=os.path.join(os.path.dirname(os.path.abspath(puma_working_dir)),"ORCA_CT_DICOM"),
                                series_description="orca co-registered CT",
                                vendor="sms",
                                force_overwrite=False)


def run_moose(ct_dir: str, mask_dir: str):
    """
    Runs moosez on the CT image in the ct_dir (EXPECTS ONLY ONE CT IMAGE)
    :param ct_dir: The directory containing the CT images
    :param mask_dir: The directory containing the masks
    """
    moose(model_name=constants.MOOSE_MODEL,
          input_dir=ct_dir,
          output_dir=mask_dir,
          accelerator=resources.check_cuda())
    # get the mask file
    mask_file = glob.glob(os.path.join(mask_dir, '*.nii*'))[0]
    # make every non-zero voxel in the mask file as 1 and the background as 0
    mask = nibabel.load(mask_file).get_fdata()
    mask[mask > 0] = 1
    # write the mask file with the same name
    nibabel.save(nibabel.Nifti1Image(mask, nibabel.load(mask_file).affine), mask_file)

def process_mask(mask_dir: str) -> None:
    """
    Processes the mask files in the mask_dir
    :param mask_dir: The directory containing the mask files
    """
    # ORCA is only using the mask of the resampled CT, the reference space is that of PET
    mask_files = sorted(glob.glob(os.path.join(mask_dir, '*.nii*')))
    with Progress() as progress:
        task = progress.add_task("[cyan] Processing mask files ", total=len(mask_files))

        # For each mask create two masks, with binary dilations of 2 and 2+8
        for mask_file in mask_files:
            mask = nibabel.load(mask_file).get_fdata()
            mask[mask > 0] = 1
            mask_dil2 = binary_dilation(mask, iterations=2).astype(dtype=np.int32)
            mask_dil8 = binary_dilation(mask_dil2, iterations=8).astype(dtype=np.int32)
            nibabel.save(nibabel.Nifti1Image(mask_dil2, nibabel.load(mask_file).affine), \
                            os.path.join(mask_dir, 'dil2_' + os.path.basename(mask_file)))
            nibabel.save(nibabel.Nifti1Image(mask_dil8, nibabel.load(mask_file).affine), \
                            os.path.join(mask_dir, 'dil8_' + os.path.basename(mask_file)))
            progress.update(task, advance=1)

