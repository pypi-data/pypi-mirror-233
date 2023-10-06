#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# **********************************************************************************************************************
# File: train.py
# Project: Optimized Registration through Conditional Adversarial networks (ORCA)
# Created: April 11, 2023, 12:01h
# Authors: Zacharias Chalampalakis, Lalith Kumar Shiyam Sundar
# Email: zacharias.chalampalakis@meduniwien.ac.at, lalith.shiyamsundar@meduniwien.ac.at
# Institute: Quantitative Imaging and Medical Physics, Medical University of Vienna
# Description:
# License: Apache 2.0
# **********************************************************************************************************************

# Importing required libraries
import sys
import os
import torch
import torch.optim as optim
import torch.nn as nn
import glob
import logging
from math import log10
import tqdm

from orcaz.generators import *
from orcaz.discriminators import *
from orcaz.train_utils import *
from orcaz.file_utilities import *
from orcaz.train_utils import *
import orcaz.NiftiDataset as NiftiDataset
from orcaz.NiftiDataset import *
from orcaz.plot_generated_batch import plot_generated_batch
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter


def train(opt):

    # TODO: Selectively get device number
    if (opt.gpu_id != -1) & torch.cuda.is_available():
        #device = torch.device("cuda:0")
        os.environ["CUDA_VISIBLE_DEVICES"] = opt.gpu_id
    
    create_directory(opt.checkpoints_dir)
    output_dir = Path(opt.checkpoints_dir)
    save_model_weights_path = output_dir / opt.run_dir

    if save_model_weights_path.exists() and (save_model_weights_path / "checkpoint.pth").exists():
        resume = True
    else:
        resume = False
    save_model_weights_path.mkdir(exist_ok=True)

    # -----  Loading the list of data -----
    train_list = create_list(opt.data_path + "/train",opt.use_tofNacData)
    val_list = create_list(opt.data_path + "/val",opt.use_tofNacData)

    for i in range(opt.increase_factor_data):  # augment the data list for training
        train_list.extend(train_list)
        val_list.extend(val_list)

    print('Number of training patches per epoch:', len(train_list))
    print('Number of validation patches per epoch:', len(val_list))
    # -------------------------------------

    ############## TENSORBOARD ########################
    from torch.utils.tensorboard import SummaryWriter
    # default `log_dir` is "runs" - we'll be more specific here
    writer_train = SummaryWriter(str(save_model_weights_path)+"/train/")
    writer_val = SummaryWriter(str(save_model_weights_path)+"/val/")
    ###################################################

    # -----  Transformation and Augmentation process for the data  -----
    min_pixel = int(opt.min_pixel * ((opt.patch_size[0] * opt.patch_size[1] * opt.patch_size[2]) / 100))
    trainTransforms = [
                NiftiDataset.Resample(opt.new_resolution, opt.resample),
                NiftiDataset.Augmentation(),
                NiftiDataset.Padding((opt.patch_size[0], opt.patch_size[1], opt.patch_size[2])),
                NiftiDataset.RandomCrop((opt.patch_size[0], opt.patch_size[1], opt.patch_size[2]), opt.drop_ratio, min_pixel),
                ]

    train_set = NifitDataSet(train_list, direction=opt.direction, transforms=trainTransforms, train=True)    # define the dataset and loader
    train_loader = DataLoader(train_set, batch_size=opt.batch_size, shuffle=True, num_workers=opt.workers)  # Here are then fed to the network with a defined batch size

    valTransforms = [
        NiftiDataset.Resample(opt.new_resolution, opt.resample),
        NiftiDataset.Padding((opt.patch_size[0], opt.patch_size[1], opt.patch_size[2])),
        NiftiDataset.RandomCrop((opt.patch_size[0], opt.patch_size[1], opt.patch_size[2]), opt.drop_ratio, min_pixel),
    ]

    val_set = NifitDataSet(val_list, direction=opt.direction, transforms=valTransforms, test=True)
    val_loader = DataLoader(val_set, batch_size=opt.batch_size, shuffle=False, num_workers=opt.workers)


    # -----  Creating the Generator, discriminator and optimizers/schedulers -----
    generator = build_netG(opt)
    discriminator = build_netD(opt)

    criterionMSE = nn.MSELoss()  # nn.MSELoss()
    criterionGAN = GANLoss()
    criterion_pixelwise = nn.L1Loss()
    # -----  Use Single GPU or Multiple GPUs -----
    if (opt.gpu_id != -1) & torch.cuda.is_available():
        use_gpu = True
        generator.cuda()
        discriminator.cuda()
        criterionGAN.cuda()
        criterion_pixelwise.cuda()

        # if num_gpus > 1:
        #     generator = nn.DataParallel(generator)
        #     discriminator = nn.DataParallel(discriminator)

    optim_generator = optim.Adam(generator.parameters(), betas=(0.5,0.999), lr=opt.generatorLR)
    optim_discriminator = optim.Adam(discriminator.parameters(), betas=(0.5,0.999), lr=opt.discriminatorLR)
    net_g_scheduler = get_scheduler(optim_generator, opt)
    net_d_scheduler = get_scheduler(optim_discriminator, opt)

    if resume:
        print(f"Using checkpoint!")
        checkpoint = torch.load(str(save_model_weights_path / "checkpoint.pth"))
        generator.load_state_dict(checkpoint["state_dict"])
        discriminator.load_state_dict(checkpoint["discriminator"])
        optim_generator.load_state_dict(checkpoint["optimizer_g"])
        optim_discriminator.load_state_dict(checkpoint["optimizer_d"])
        net_g_scheduler.load_state_dict(checkpoint["net_g_scheduler"])
        net_d_scheduler.load_state_dict(checkpoint["net_d_scheduler"])
        epoch_count= checkpoint["epoch"]
    else:
        epoch_count = opt.epoch_count

    # -----  Training Cycle -----
    logging.info('Start training :) ')
    
    for epoch in range(epoch_count, opt.niter + opt.niter_decay):
        mean_generator_total_loss = 0.0
        mean_discriminator_loss = 0.0
        step = 0
        generator.train()

        pbar = tqdm.tqdm(enumerate(train_loader), total=len(train_loader))
        for batch_idx, (data, label) in pbar:

            real_a = data
            real_b = label

            if use_gpu:                              # forward
                real_b = real_b.cuda()
                fake_b = generator(real_a.cuda())    # generate fake data
                real_a = real_a.cuda()
            else:
                fake_b = generator(real_a)

            ######################
            # (1) Update D network
            ######################
            optim_discriminator.zero_grad()

            # train with fake
            fake_ab = torch.cat((real_a, fake_b), 1)
            pred_fake = discriminator.forward(fake_ab.detach())
            loss_d_fake = criterionGAN(pred_fake, False)

            # train with real
            real_ab = torch.cat((real_a, real_b), 1)
            pred_real = discriminator.forward(real_ab)
            loss_d_real = criterionGAN(pred_real, True)

            # Combined D loss
            discriminator_loss = (loss_d_fake + loss_d_real) * 0.5

            mean_discriminator_loss += discriminator_loss
            discriminator_loss.backward()
            optim_discriminator.step()

            ######################
            # (2) Update G network
            ######################

            optim_generator.zero_grad()

            # First, G(A) should fake the discriminator
            fake_ab = torch.cat((real_a, fake_b), 1)
            pred_fake = discriminator.forward(fake_ab)
            loss_g_gan = criterionGAN(pred_fake, True)

            # Second, G(A) = B
            loss_g_l1 = criterion_pixelwise(fake_b, real_b) * opt.lamb

            generator_total_loss = loss_g_gan + loss_g_l1

            mean_generator_total_loss += generator_total_loss
            generator_total_loss.backward()
            optim_generator.step()

            ######### Status and display #########
            pbar.set_postfix(
            {
                "epoch": epoch_count,
                "Discriminator_Loss": f"{discriminator_loss:.6f}",
                "Generator_Loss": f"{generator_total_loss:.6f}",
                # "p_loss": f"{losses['p_loss'].item():.6f}",
                # "g_loss": f"{losses['g_loss'].item():.6f}",
                # "d_loss": f"{losses['d_loss'].item():.6f}",
                # "lr_g": f"{get_lr(optimizer_g):.6f}",
                # "lr_d": f"{get_lr(optimizer_d):.6f}",
            })

        update_learning_rate(net_g_scheduler, optim_generator)
        update_learning_rate(net_d_scheduler, optim_discriminator)

        ##### Logger ######
        mean_generator_total_loss /= len(train_loader)
        mean_discriminator_loss /= len(train_loader)

        if (epoch) % opt.val_fre == 0:
            plot_generated_batch(val_list=val_list, model=generator, resample=opt.resample, resolution=opt.new_resolution,
                                patch_size_x=opt.patch_size[0], patch_size_y=opt.patch_size[1],
                                patch_size_z=opt.patch_size[2], stride_inplane=opt.stride_inplane,
                                stride_layer=opt.stride_layer, batch_size=1,
                                epoch=epoch_count, save_model_weights_path=save_model_weights_path)

        ############## TENSORBOARD ########################
        writer_train.add_scalar('generator_total_loss',
                            mean_generator_total_loss.cpu().item(), epoch)
        writer_train.add_scalar('discriminator_loss',
                            mean_discriminator_loss.cpu().item(), epoch)
        ###################################################
    
        epoch_count += 1
        if epoch % opt.save_fre == 0:
            torch.save(generator.state_dict(), '%s/g_epoch_{}.pth'.format(epoch) % save_model_weights_path)
            torch.save(discriminator.state_dict(), '%s/d_epoch_{}.pth'.format(epoch) % save_model_weights_path)

            # Save checkpoint
            checkpoint = {
                "epoch": epoch_count,
                "state_dict": generator.state_dict(),
                "discriminator": discriminator.state_dict(),
                "optimizer_g": optim_generator.state_dict(),
                "optimizer_d": optim_discriminator.state_dict(),
                "net_g_scheduler": net_g_scheduler.state_dict(),
                "net_d_scheduler": net_d_scheduler.state_dict()
            }
            torch.save(checkpoint, str(save_model_weights_path / "checkpoint.pth"))

        # sys.stdout.write(
        #     '\r[%d/%d] Discriminator_Loss: %.4f Generator_Loss:%.4f \n' % (
        #         epoch_count-1, (opt.niter + opt.niter_decay + 1),
        #         mean_discriminator_loss / len(train_loader),
        #         mean_generator_total_loss / len(train_loader)
        #         ))
