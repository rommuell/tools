#!/usr/bin/python
#! -*- encoding: utf-8 -*-

# Python script for okvis / openMVG interface
#
# SfM from okvis data
# modified Roman Mueller, 06/1/2016



import commands
import os
import subprocess
import sys
import time
import numpy as np
import csv
import shutil

# settings
OPENMVG_SFM_BIN = "/home/rm/openMVG_Build/Linux-x86_64-Release"
path = '/home/rm/Documents/master_thesis/data/okvis_output'
# end settings


#################################################################################
# List Matches from okvis output
# set: path, maxWindow
if 1:
    execfile( "okvisToMatches.py")


#################################################################################
# openMVG image listing & change intrinsics
if 1:
    pIntrisics = subprocess.Popen( [OPENMVG_SFM_BIN + '/openMVG_main_SfMInit_ImageListing',
                                    "-i", path,
                                    "-o", path + '/matches',
                                    "-f", "100" # placeholder, is replaced later
                                    ] )
    pIntrisics.wait()

    # open image list
    with open(path + '/matches/sfm_data.json') as sfmFile:
        sfm_list = sfmFile.read().splitlines()
    sfmFile.close()

    # open file with custom intrinsics
    with open('/home/rm/Documents/master_thesis/src/tools/config_fpga_v4r4.intr') as intrFile:
        intr_list = intrFile.read().splitlines()
    intrFile.close()

    # merge lists
    sfm_list = sfm_list[:len(sfm_list)-30]
    sfm_list.extend(intr_list)

    # open overwrite image list
    with open(path + '/matches/sfm_data.json', 'w+') as sfmFile:
        sfmFile.writelines('\n'.join(sfm_list))
    sfmFile.close()

    #copy image describer file
    shutil.copy('/home/rm/Documents/master_thesis/src/tools/image_describer.json', path + '/matches')


#################################################################################
if 0: # if camera poses from okvis
    execfile('okvisToExtrinsics.py')


#################################################################################
# call openMVG_Compute_Matches to filter matches / generate graphs
if 0:
    tic = time.time()

    pMatches = subprocess.Popen( [OPENMVG_SFM_BIN + '/openMVG_main_ComputeMatches',
                                  "-i", path + "/matches/sfm_data.json",
                                  "-o", path + '/matches',
                                  "-n", "FASTCASCADEHASHINGL2"
                                  ] )
    pMatches.wait()
    t_matches = time.time() - tic


#################################################################################
# reconstruction without extrinsics
if 1:
    tic = time.time()

    reconstruction_dir = path + '/reconstruction_sequential'
    if not os.path.exists(reconstruction_dir):
        os.mkdir(reconstruction_dir)

    pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, 'openMVG_main_IncrementalSfM'),
                                 '-a', '00001550.png',
                                 '-b', '00001771.png',
                                 '-i', path + '/matches/sfm_data.json',
                                 '-m', path + '/matches',
                                 '-o', reconstruction_dir
                                 ] )

#################################################################################
# reconstruction with given extrinsics
if 0:
    pPoses = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeStructureFromKnownPoses"),
                                "-i", path +"/matches/sfm_data_pose.json",
                                "-m", path + '/matches',
                                "-o", os.path.join(reconstruction_dir,"robust.ply")
                                ] )
    pPoses.wait()

#pRecons.wait()
#t_reconstruction = time.time() - tic

#tic = time.time()
#print ("5. Colorize Structure")
#pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeSfM_DataColor"), 
#	"-i", reconstruction_dir+"/sfm_data.bin", 
#	"-o", os.path.join(reconstruction_dir,"colorized.ply")] )
#pRecons.wait()
#t_colorize = time.time() - tic

#print( "Intrinsic", t_intrinsic)
#print( "Features", t_features)
#print( "Matches", t_matches)
#print( "Inc. reconstruction", t_reconstruction)
#print( "Colorize", t_colorize)
#print( "total time:", t_intrinsic + t_features + t_matches + t_reconstruction + t_colorize)

##print ("4. Structure from Known Poses (robust triangulation)")
##pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeStructureFromKnownPoses"),  "-i", reconstruction_dir+"/sfm_data.bin", "-m", matches_dir, "-o", os.path.join(reconstruction_dir,"robust.ply")] )
##pRecons.wait()


#print ("Convert .bin to .json")
#pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ConvertSfM_DataFormat"),
#	"-i", reconstruction_dir+"/sfm_data.bin",
#	"-o", reconstruction_dir+"/sfm_data.json"] )
#pRecons.wait()
