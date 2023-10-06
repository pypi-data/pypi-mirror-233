import SimpleITK as sitk
import matplotlib.pyplot as plt
from orcaz.NiftiDataset import *
import orcaz.NiftiDataset as NiftiDataset
from orcaz.predict_single_image import inference
from numpy.random import randint

def plot_generated_batch(val_list, model, resample, resolution, patch_size_x, patch_size_y, patch_size_z, stride_inplane, 
stride_layer, batch_size, epoch,save_model_weights_path):
    # --------------- reading the images from the validation list --------------

    image = val_list[0]['data']
    label = val_list[0]['label']

    # ------------------------------------------------------------------------------

    result, dice = inference(False, model, image, None, 'prova.nii', resample, resolution, patch_size_x,
                       patch_size_y, patch_size_z, stride_inplane, stride_layer, batch_size, segmentation=False)

    # save
    #writer = sitk.ImageFileWriter()
    # label_directory = 'checkpoints/Epochs_training/epoch_%s' % epoch
    # if not os.path.exists(label_directory):
    #     os.makedirs(label_directory)
    #label_directory = os.path.join(label_directory, 'epoch_prediction.nii.gz')
    #writer.SetFileName(label_directory)
    #writer.Execute(result)

    # --------------------------- Plotting samples during training ---------------------------------

    first_mod, second_mod, predicted = sitk.ReadImage(image), sitk.ReadImage(label), result

    first_mod = sitk.GetArrayFromImage(first_mod)
    second_mod = sitk.GetArrayFromImage(second_mod)
    predicted = sitk.GetArrayFromImage(result)

    _1 = int(randint(0, first_mod.shape[0], 1) - 1)
    _2 = int(randint(0, first_mod.shape[0], 1) - 1)
    _3 = int(randint(0, first_mod.shape[0], 1) - 1)
    _4 = int(randint(0, first_mod.shape[0], 1) - 1)

    fig = plt.figure()
    fig.set_size_inches(12, 12)

    plt.subplot(5, 3, 1), plt.imshow(first_mod[_1], 'gray'), plt.axis('off'), plt.title('PET')
    plt.subplot(5, 3, 2), plt.imshow(predicted[_1], 'gray'), plt.axis('off'), plt.title('GAN sCT')
    plt.subplot(5, 3, 3), plt.imshow(second_mod[_1], 'gray'), plt.axis('off'), plt.title('CT')

    plt.subplot(5, 3, 4), plt.imshow(first_mod[_2], 'gray'), plt.axis('off'), plt.title('PET')
    plt.subplot(5, 3, 5), plt.imshow(predicted[_2], 'gray'), plt.axis('off'), plt.title('GAN sCT')
    plt.subplot(5, 3, 6), plt.imshow(second_mod[_2], 'gray'), plt.axis('off'), plt.title('CT')

    plt.subplot(5, 3, 7), plt.imshow(first_mod[_3], 'gray'), plt.axis('off'), plt.title('PET')
    plt.subplot(5, 3, 8), plt.imshow(predicted[_3], 'gray'), plt.axis('off'), plt.title('GAN sCT')
    plt.subplot(5, 3, 9), plt.imshow(second_mod[_3], 'gray'), plt.axis('off'), plt.title('CT')

    plt.subplot(5, 3, 10), plt.imshow(first_mod[_4], 'gray'), plt.axis('off'), plt.title('PET')
    plt.subplot(5, 3, 11), plt.imshow(predicted[_4], 'gray'), plt.axis('off'), plt.title('GAN sCT')
    plt.subplot(5, 3, 12), plt.imshow(second_mod[_4], 'gray'), plt.axis('off'), plt.title('CT')

    # plt.subplot(5, 3, 13, autoscale_on=True), plt.hexbin((first_mod / first_mod.max()), (second_mod / second_mod.max()),
    #                                                      bins='log', cmap=plt.cm.Blues,gridsize=50), plt.title('NMI')

    plt.subplot(5, 3, 14, autoscale_on=True), plt.hexbin((predicted), (second_mod),
                                                         bins='log', cmap=plt.cm.Blues,gridsize=50), plt.title('NMI')

    # plt.subplot(5, 3, 15, autoscale_on=True), plt.hexbin((second_mod / second_mod.max()), (second_mod / second_mod.max()), bins='log',
    #                                                      cmap=plt.cm.Blues,gridsize=50), plt.title('NMI')

    plt.savefig('%s/Epoch_{}.png'.format(epoch) % save_model_weights_path)
    plt.close()