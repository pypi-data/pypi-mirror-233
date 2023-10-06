#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# **********************************************************************************************************************
# File: display.py
# Project: 
# Created: April 11, 2023, 13:03h
# Author: Lalith Kumar Shiyam Sundar
# Email: lalith.shiyamsundar@meduniwien.ac.at
# Institute: Quantitative Imaging and Medical Physics, Medical University of Vienna
# Description: A module for displaying the messages of the wolfz processing.
# License: Apache 2.0
# **********************************************************************************************************************

# Importing required libraries

import pyfiglet
from orcaz import constants


def logo():
    """
    Display WOLFZ logo
    :return:
    """
    print(' ')
    logo_color_code = constants.ANSI_BLUE
    slogan_color_code = constants.ANSI_BLUE
    result = logo_color_code + pyfiglet.figlet_format("ORCA 0.1.2", font="slant").rstrip() + "\033[0m"
    text = slogan_color_code + " A part of the ENHANCE-PET framework." + "\033[0m"
    print(result)
    print(text)
    print(' ')


def expectations():
    """
    Display the expectations for the program to run
    :return:
    """
    print(' ')
    print(
        constants.ANSI_ORANGE + " Please make sure that the following conditions are met before running the program:" + constants.ANSI_RESET)
    print(' ')
    print(constants.ANSI_ORANGE + " 1. The subject directory should contain more than one imaging session." +
          constants.ANSI_RESET)
    print(' ')
    print(constants.ANSI_ORANGE + " 2. The subject session should exactly contain one PET and one CT image." +
          constants.ANSI_RESET)
    print(' ')
