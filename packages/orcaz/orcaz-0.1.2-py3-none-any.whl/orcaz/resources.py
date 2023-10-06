#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------------------------------------------------
# Author: Lalith Kumar Shiyam Sundar | Sebastian Gutschmayer
# Institution: Medical University of Vienna
# Research Group: Quantitative Imaging and Medical Physics (QIMP) Team
# Date: 04.07.2023
# Version: 0.1.0
#
# Description:
# This module contains the urls and filenames of the binaries that are required for the orca.
#
# Usage:
# The variables in this module can be imported and used in other modules within the orca to download the necessary
# binaries for the orca.
#
# ----------------------------------------------------------------------------------------------------------------------
import torch
from orcaz import constants

# ORCA MODELS

ORCA_MODELS = {
    "nac_fdg_pet": {
        "url": "https://orca.s3.eu.cloud-object-storage.appdomain.cloud/nac_fdg_pet_03082023.zip",
        "filename": "nac_fdg_pet.zip",
        "model": "NAC_FDG_ORCA.pth",
        "directory": "nac_fdg_pet",
    },
    "ac_fdg_pet": {
        "url": "https://orca.s3.eu.cloud-object-storage.appdomain.cloud/ac_fdg_pet_03082023.zip",
        "filename": "ac_fdg_pet.zip",
        "model": "AC_FDG_ORCA.pth",
        "directory": "ac_fdg_pet",
    },
}


def check_cuda(print_flag=False) -> str:
    """
    This function checks if CUDA is available on the device and prints the device name and number of CUDA devices
    available on the device.

    Returns:
        str: The device to run predictions on, either "cpu" or "cuda".
    """
    if not torch.cuda.is_available():
        print(
            f"{constants.ANSI_ORANGE}CUDA not available on this device. Predictions will be run on CPU.{constants.ANSI_RESET}") if print_flag else None
        return "cpu"
    else:
        device_count = torch.cuda.device_count()
        print(
            f"{constants.ANSI_GREEN} CUDA is available on this device with {device_count} GPU(s). Predictions will be run on GPU.{constants.ANSI_RESET}") if print_flag else None
        return "cuda"
