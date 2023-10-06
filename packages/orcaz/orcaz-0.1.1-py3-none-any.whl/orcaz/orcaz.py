#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# **********************************************************************************************************************
# File: orca.py
# Project: Optimized Registration through Conditional Adversarial networks (ORCA)
# Author: Zacharias Chalampalakis | Lalith Kumar Shiyam Sundar | Sebastian Gutschmayer
# Institution: Medical University of Vienna
# Research Group: Quantitative Imaging and Medical Physics (QIMP) Team
# Date: 04.07.5023
# Version: 0.1.0
# Email: zacharias.chalampalakis@meduniwien.ac.at, lalith.shiyamsundar@meduniwien.ac.at
# Description: 
# ORCA is a deep learning based image registration framework for the co-registration between CT and PET images.
# License: Apache 2.0
# Usage:
# python orca.py --mode coreg --ct /path/to/ct.nii.gz --pet /path/to/pet.nii.gz --dout /path/to/output_dir
# python orca.py --mode pred --pet /path/to/pet.nii.gz --dout /path/to/output_dir
# python orca.py --mode train --data_path /path/to/data --output /path/to/checkpoints_dir
# **********************************************************************************************************************

# Importing required libraries
import logging
import sys
import emoji
import time

from datetime import datetime
from orcaz import train
from orcaz import predict_single_image
from orcaz import display,constants,file_utilities
from orcaz import download,resources
from orcaz.options import Options
from orcaz import image_conversion
from orcaz import settings
from orcaz import image_processing
import os 
import glob
import falconz.resources as falcon_resources

import warnings
warnings.filterwarnings('ignore', category=UserWarning, message='TypedStorage is deprecated')

import resource
rlimit = resource.getrlimit(resource.RLIMIT_NOFILE)
resource.setrlimit(resource.RLIMIT_NOFILE, (4096, rlimit[1]))

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', level=logging.INFO,
                    filename=datetime.now().strftime('orca-%H-%M-%d-%m-%Y.log'),
                    filemode='w')
# uncomment the following line to print the logs to the console
#logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

def main():

    display.logo()
    logging.info("----------------------------------------------------------------------------------------------------")
    logging.info("                                         STARTING ORCA 0.1.0                                        ")
    logging.info("----------------------------------------------------------------------------------------------------")
    logging.info(' ')

    # ----------------------------------
    # DOWNLOADING THE BINARIES
    # ----------------------------------

    print('')
    print(f'{constants.ANSI_BLUE} {emoji.emojize(":globe_with_meridians:")} BINARIES DOWNLOAD:{constants.ANSI_RESET}')

    print('')
    binary_path = constants.BINARY_PATH
    file_utilities.create_directory(binary_path)
    system_os, system_arch = file_utilities.get_system()
    print(f'{constants.ANSI_ORANGE} Detected system: {system_os} | Detected architecture: {system_arch}'
          f'{constants.ANSI_RESET}')
    download.download(item_name=f'falcon-{system_os}-{system_arch}', item_path=binary_path,
                      item_dict=falcon_resources.FALCON_BINARIES)
    file_utilities.set_permissions(constants.FALCON_PATH, system_os)

    # ----------------------------------
    # INPUT ARGUMENTS and SWITCH BETWEEN MODES
    # ----------------------------------

   
    opt = Options().parse_options()
    if opt.mode =='train':
        logging.info('-'*50)
        logging.info('          Using ORCA in training mode             ')
        logging.info('-'*50)
        train.train(opt)

    elif opt.mode =='generate':
        logging.info('-'*50)
        logging.info('          Using ORCA in prediction mode           ')
        logging.info('-'*50)
        # ----------------------------------
        # INPUT STANDARDIZATION
        # ----------------------------------
        print('')
        print(f'{constants.ANSI_BLUE} {emoji.emojize(":magnifying_glass_tilted_left:")} STANDARDIZING INPUT DATA TO '
            f'NIFTI:{constants.ANSI_RESET}')
        print('')
        logging.info(' ')
        logging.info(' STANDARDIZING INPUT DATA:')
        logging.info(' ')
        sub_dirs = image_conversion.standardize_to_nifti(opt.subject_directory)
        print(f"{constants.ANSI_GREEN} Standardization complete.{constants.ANSI_RESET}")
        logging.info(" Standardization complete.")
        if 'AC_FDG_PET' in sub_dirs:
            models_path = constants.MODEL_PATH
            file_utilities.create_directory(models_path)
            download.download(item_name='ac_fdg_pet', item_path=constants.MODEL_PATH, item_dict=resources.ORCA_MODELS)
            settings.model_path = os.path.join(constants.MODEL_PATH,resources.ORCA_MODELS['ac_fdg_pet']['directory'],resources.ORCA_MODELS['ac_fdg_pet']['model'])

        elif 'NAC_FDG_PET' in sub_dirs:
            models_path = constants.MODEL_PATH
            file_utilities.create_directory(models_path)
            download.download(item_name='nac_fdg_pet', item_path=constants.MODEL_PATH, item_dict=resources.ORCA_MODELS)
            settings.model_path = os.path.join(constants.MODEL_PATH,resources.ORCA_MODELS['nac_fdg_pet']['directory'],resources.ORCA_MODELS['nac_fdg_pet']['model'])

        else:
            # print error unrecognized subdirectories structure
            logging.error("*** !Unrecognized subdirectories, exiting now! ***")
            return 1;

        # -------------------------------------------------
        # RUNNING PREPROCESSING AND PREDICTION PIPELINE
        # -------------------------------------------------
        # calculate elapsed time for the entire procedure below
        start_time = time.time()
        print('')
        print(f'{constants.ANSI_VIOLET} {emoji.emojize(":rocket:")} RUNNING PREPROCESSING AND GENERATION PIPELINE:{constants.ANSI_RESET}')
        print('')
        logging.info(' ')
        logging.info(' RUNNING PREPROCESSING AND GENERATION PIPELINE:')
        logging.info(' ')
        orca_dir, ct_dir, pt_dir, mask_dir = image_processing.preprocess(opt.subject_directory)
        print(f'{constants.ANSI_GREEN} {emoji.emojize(":hourglass_done:")} Preprocessing complete.{constants.ANSI_RESET}')
        print(f'{constants.ANSI_VIOLET} {emoji.emojize(":robot:")} Generating syntheticCT .{constants.ANSI_RESET}')
        predict_single_image.predict(opt, orca_dir, ct_dir, pt_dir)
        end_time = time.time()
        elapsed_time = end_time - start_time
        # show elapsed time in minutes and round it to 2 decimal places
        elapsed_time = round(elapsed_time / 60, 2)
        print(f'{constants.ANSI_GREEN} {emoji.emojize(":hourglass_done:")} synthetic CT generation complete.'
            f' Elapsed time: {elapsed_time} minutes! {emoji.emojize(":partying_face:")} \n Generated images are stored in'
            f' {orca_dir}! {constants.ANSI_RESET}')
   
    elif opt.mode=='coreg':
        logging.info('-'*50)
        logging.info('        Using ORCA in co-registration mode        ')
        logging.info('-'*50)

        # ----------------------------------
        # INPUT STANDARDIZATION
        # ----------------------------------
        # calculate elapsed time for the entire procedure below
        start_time = time.time()
        print('')
        print(f'{constants.ANSI_BLUE} {emoji.emojize(":magnifying_glass_tilted_left:")} STANDARDIZING INPUT DATA TO '
            f'NIFTI:{constants.ANSI_RESET}')
        print('')
        logging.info(' ')
        logging.info(' STANDARDIZING INPUT DATA:')
        logging.info(' ')
        sub_dirs = image_conversion.standardize_to_nifti(opt.subject_directory)
        print(f"{constants.ANSI_GREEN} Standardization complete.{constants.ANSI_RESET}")
        logging.info(" Standardization complete.")
        
        if len(sub_dirs) == 2:
            if 'CT' in sub_dirs and 'AC_FDG_PET' in sub_dirs:
                models_path = constants.MODEL_PATH
                file_utilities.create_directory(models_path)
                download.download(item_name='ac_fdg_pet', item_path=constants.MODEL_PATH, item_dict=resources.ORCA_MODELS)
                settings.model_path = os.path.join(constants.MODEL_PATH,resources.ORCA_MODELS['ac_fdg_pet']['directory'],resources.ORCA_MODELS['ac_fdg_pet']['model'])
            elif 'CT' in sub_dirs and 'NAC_FDG_PET' in sub_dirs:
                models_path = constants.MODEL_PATH
                file_utilities.create_directory(models_path)
                download.download(item_name='nac_fdg_pet', item_path=constants.MODEL_PATH, item_dict=resources.ORCA_MODELS)
                settings.model_path = os.path.join(constants.MODEL_PATH,resources.ORCA_MODELS['nac_fdg_pet']['directory'],resources.ORCA_MODELS['nac_fdg_pet']['model'])
            else:
                # print error unrecognized subdirectories structure
                logging.error("*** !Unrecognized subdirectories structure, exiting now! ***")
                return 1;
        
        # ---------------------------------------------------
        # RUNNING PREPROCESSING AND CO-REGISTRATION PIPELINE
        # ---------------------------------------------------
        start_time = time.time()
        print('')
        print(f'{constants.ANSI_VIOLET} {emoji.emojize(":rocket:")} RUNNING PREPROCESSING AND CO-REGISTRATION PIPELINE:{constants.ANSI_RESET}')
        print('')

        logging.info(' ')
        logging.info(' RUNNING PREPROCESSING AND CO-REGISTRATION PIPELINE:')
        logging.info(' ')
        orca_dir, ct_dir, pt_dir, mask_dir = image_processing.preprocess(opt.subject_directory)
        print(f'{constants.ANSI_GREEN} {emoji.emojize(":hourglass_done:")} Preprocessing complete.{constants.ANSI_RESET}')
        print(f'{constants.ANSI_VIOLET} {emoji.emojize(":robot:")} Generating syntheticCT.{constants.ANSI_RESET}')
        predict_single_image.predict(opt, orca_dir, ct_dir, pt_dir)
        print(f'{constants.ANSI_GREEN} {emoji.emojize(":hourglass_done:")} synthetic CT generation complete.{constants.ANSI_RESET}')
        print(f'{constants.ANSI_VIOLET} {emoji.emojize(":whale:")} Co-registering CT to synthetic CT.{constants.ANSI_RESET}')
        image_processing.align(orca_dir, ct_dir, pt_dir, mask_dir,opt.workers)
        image_processing.postprocess(orca_dir, ct_dir, mask_dir)
        # Check if input ct is in DICOM format, if so export the co-registered CT to DICOM
        subject_directory = os.path.abspath(opt.subject_directory)

        if image_conversion.is_dicom(glob.glob(os.path.join(subject_directory, 'CT/*'))[0]):
            image_processing.export_dicom(orca_dir, ct_dir)
        end_time = time.time()
        elapsed_time = end_time - start_time
        # show elapsed time in minutes and round it to 2 decimal places
        elapsed_time = round(elapsed_time / 60, 2)
        print(f'{constants.ANSI_GREEN} {emoji.emojize(":hourglass_done:")} Co-registration complete.'
            f' Elapsed time: {elapsed_time} minutes! {emoji.emojize(":partying_face:")} \n Co-registered images are stored in'
            f' {constants.ALIGNED_CT_FOLDER}! {constants.ANSI_RESET}')


    else:
        logging.error("*** !Unknown mode option requested, exiting now! ***")
        print(f'{constants.ANSI_ORANGE} {emoji.emojize(":warning:")} Unknown mode option requested, exiting now! {constants.ANSI_RESET}')
        return 1; 

if __name__ == '__main__':
  main()