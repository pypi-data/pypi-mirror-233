import subprocess
import os
import time
from orcaz.file_utilities import *

INITIAL = f'initial'
BONES = f'bones'
ORGANS = f'organs'
TISSUE = f'tissue'
RIGID = f'rigid'
AFFINE = f'affine'
DEFORMABLE = f'deformable'


def filter(moving_img: str, filtered_img: str) -> None:
    """
    Performs filtering of the moving image to match filtering used in training datasets.
    """ #c3d ${3} -smooth 2x2x2mm -o ${1}/$moco_dir/filtered_moving_image.nii.gz 
    
    command_string = f"c3d " \
                     f"{moving_img} " \
                     f"-smooth 2x2x2mm " \
                     f"-o " \
                     f"{filtered_img} "
    
    print(command_string)
    subprocess.run(command_string, shell=True, capture_output=subprocess.DEVNULL)

def rigid(fixed_img: str, moving_img: str, registration_sequence: str, directory: str,cost_function: str, multi_resolution_iterations: str, nb_threads: int) -> None:
    """
    Performs rigid registration between a fixed and moving image using the greedy registration toolkit
    """
    # check if there is an initial transform
    initial_transform_command = f"-ia-image-centers "
    initial_transform_path = "None"
    if os.path.exists(os.path.join(directory, f"{INITIAL}.mat")):
        initial_transform_path = os.path.join(directory, f"{INITIAL}.mat")
        initial_transform_command = f"-ia {initial_transform_path} "

    transform_file_path = os.path.join(directory, f"{registration_sequence}_rigid.mat")
    if registration_sequence == INITIAL:
        transform_file_path = os.path.join(directory, f"{INITIAL}.mat")

    print(f'[GREEDY]    Initial transform: {initial_transform_path}, Output transform: {transform_file_path}')
    command_string = f"greedy " \
                     f"-d 3 " \
                     f"-a " \
                     f"{initial_transform_command}" \
                     f"-i {fixed_img} {moving_img} " \
                     f"-dof 6 " \
                     f"-o {transform_file_path} " \
                     f"-n {multi_resolution_iterations} " \
                     f"-m {cost_function} " \
                     f"-threads {nb_threads} " \
    
    subprocess.run(command_string, shell=True, capture_output=subprocess.DEVNULL)


def affine(fixed_img: str, moving_img: str, registration_sequence: str, directory: str, cost_function: str, multi_resolution_iterations: str, nb_threads: int) -> None:
    """
    Performs affine registration between a fixed and moving image using the greedy registration toolkit
    """
    # check if there is an initial transform
    initial_transform_command = f"-ia-image-centers "
    initial_transform_path = "None"
    if os.path.exists(os.path.join(directory, f"{INITIAL}.mat")):
        initial_transform_path = os.path.join(directory, f"{INITIAL}.mat")
        initial_transform_command = f"-ia {initial_transform_path} "

    transform_file_path = os.path.join(directory, f"{registration_sequence}_affine.mat")
    if registration_sequence == INITIAL:
        transform_file_path = os.path.join(directory, f"{INITIAL}.mat")

    print(f'[GREEDY]    Initial transform: {initial_transform_path}, Output transform: {transform_file_path}')
    command_string = f"greedy " \
                     f"-d 3 " \
                     f"-a " \
                     f"{initial_transform_command}" \
                     f"-i {fixed_img} {moving_img} " \
                     f"-dof 12 " \
                     f"-o {transform_file_path} " \
                     f"-n {multi_resolution_iterations} " \
                     f"-m {cost_function} " \
                     f"-threads {nb_threads} "                                      
    print(command_string)
    subprocess.run(command_string, shell=True, capture_output=subprocess.DEVNULL)


def deformable(fixed_img: str, moving_img: str, registration_sequence: str, directory: str, cost_function: str, multi_resolution_iterations: str, nb_threads: int, mask_img: str) -> None:
    """
    Performs deformable registration between a fixed and moving image using the greedy registration toolkit
    """
    # check if there is an initial transform
    initial_transform_command = f""
    initial_transform_path = ""
    if os.path.exists(os.path.join(directory, f"{INITIAL}.mat")):
        initial_transform_path = os.path.join(directory, f"{INITIAL}.mat")
        initial_transform_command = f"-it {initial_transform_path} "

    transform_file_path = os.path.join(directory, f"{registration_sequence}_warp.nii.gz")
    #inverse_transform = os.path.join(directory, f"{registration_sequence}_inverse_warp.nii.gz")

    print(f'[GREEDY]    Initial transform: {initial_transform_path}, Output transform: {transform_file_path}')
    command_string = f"greedy " \
                     f"-d 3 " \
                     f"-m {cost_function} " \
                     f"{initial_transform_command}" \
                     f"-i {fixed_img} {moving_img} " \
                     f"-o {transform_file_path} " \
                     f"-n {multi_resolution_iterations} " \
                     f"-threads {nb_threads} " \
                     f"-mm {mask_img} " 
                    #f"-oinv {inverse_transform} " #
    print(command_string)
    subprocess.run(command_string, shell=True, capture_output=subprocess.DEVNULL)


def registration(fixed_img: str, moving_img: str, directory: str, registration_sequence: str, registration_type: str, multi_resolution_iterations: str) -> None:
    """
    Registers the fixed and the moving image using the greedy registration toolkit based on the user given cost function
    """

    print(f'[GREEDY]    performing {registration_type} registration for {registration_sequence} to align\n'
          f'            {moving_img} to \n'
          f'            {fixed_img}...')
    start = time.time()

    if registration_type == 'rigid':
        rigid(fixed_img, moving_img, registration_sequence, directory,
              cost_function='SSD', multi_resolution_iterations=multi_resolution_iterations)
    elif registration_type == 'affine':
        affine(fixed_img, moving_img, registration_sequence, directory,
               cost_function='SSD', multi_resolution_iterations=multi_resolution_iterations)
    elif registration_type == 'deformable':
        deformable(fixed_img, moving_img, registration_sequence, directory,
                   cost_function='SSD', multi_resolution_iterations=multi_resolution_iterations)
    else:
        exit("Registration type not supported!")

    end = time.time()
    print(f'            ... completed in {(end - start)/60}min')


def resample(fixed_img: str, moving_img: str, directory: str, registration_sequence: str, registration_type: str, resampled_img:str) -> None:
    """
    Resamples a moving image to match the resolution of a fixed image
    """
    initial_transform_command = f""
    initial_transform_path = ""
    if os.path.exists(os.path.join(directory, f"{INITIAL}.mat")):
        initial_transform_path = os.path.join(directory, f"{INITIAL}.mat")


    print(f"[GREEDY]    resampling {moving_img} based on motion correction results at {directory}.")
    print(f"            writing as {resampled_img}")

    cmd_to_run = ""
    if (registration_type == RIGID or registration_type == AFFINE) and registration_sequence == INITIAL:
        if moving_img and resampled_img:
            cmd_to_run = f"greedy " \
                         f"-d 3 " \
                         f"-rf {fixed_img} " \
                         f"-rm {moving_img} {resampled_img} " \
                         f"-r {os.path.join(directory, f'{registration_sequence}.mat')}"

    elif registration_type == RIGID:
        if moving_img and resampled_img:
            cmd_to_run = f"greedy " \
                         f"-d 3 " \
                         f"-rf {fixed_img} " \
                         f"-rm {moving_img} {resampled_img} " \
                         f"-r {os.path.join(directory, f'{registration_sequence}_rigid.mat')}"

    elif registration_type == AFFINE:
        if moving_img and resampled_img:
            cmd_to_run = f"greedy " \
                         f"-d 3 " \
                         f"-rf {fixed_img} " \
                         f"-rm {moving_img} {resampled_img} " \
                         f"-r {os.path.join(directory, f'{registration_sequence}_affine.mat')}"

    elif registration_type == DEFORMABLE:
        if moving_img and resampled_img:
            cmd_to_run = f"greedy " \
                         f"-d 3 " \
                         f"-rf {fixed_img} " \
                         f"-rm {moving_img} {resampled_img} " \
                         f"-r {os.path.join(directory, f'{registration_sequence}_warp.nii.gz')} {initial_transform_path}"
    print(cmd_to_run)
    subprocess.run(cmd_to_run, shell=True, capture_output=subprocess.DEVNULL)

# def reslice_initial(reference_image, moving_image, resclied_image, initial_transform, interpolation_type="NN"):
#     print(f"[OCELOT]                {moving_image} -> {resclied_image}")
#     print(f"[OCELOT]      Reference {reference_image} | Interpolation: {interpolation_type}")
#     command_string = f"greedy " \
#                      f"-d 3 " \
#                      f"-rf {reference_image} " \
#                      f"-ri {interpolation_type} " \
#                      f"-rm {moving_image} {resclied_image} " \
#                      f"-r {initial_transform}"
#     subprocess.run(command_string, shell=True, capture_output=True)


# def reslice_warp(reference_image, moving_image, resclied_image, warp, initial_transform="", interpolation_type="NN"):
#     print(f"[OCELOT]                {moving_image} -> {resclied_image}")
#     print(f"[OCELOT]      Reference {reference_image} | Interpolation: {interpolation_type}")

#     command_string = f"greedy " \
#                      f"-d 3 " \
#                      f"-rf {reference_image} " \
#                      f"-ri {interpolation_type} " \
#                      f"-rm {moving_image} {resclied_image} " \
#                      f"-r {warp} {initial_transform}"
#     subprocess.run(command_string, shell=True, capture_output=True)
