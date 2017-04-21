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
OPENMVG_SFM_BIN = "/home/rm/openMVG_Build/Linux-x86_64-RELEASE"
path = '/home/rm/Documents/master_thesis/data/okvis_output'
# end settings


#################################################################################
# List Matches from okvis output
# set: path, maxWindow
tic = time.time()
if 0:
    pOkToMat = subprocess.Popen( ['/home/rm/egm/build/okvisToMatches',
                                 '-i', path,
                                 ])
    pOkToMat.wait()
    #    execfile( "okvisToMatches.py")
t_oktomat = time.time() - tic

#################################################################################
# openMVG image listing & change intrinsics
tic = time.time()
if 0:
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
    with open('/home/rm/Documents/master_thesis/src/tools/config_fpga_p2_euroc.intr') as intrFile:
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

t_list = time.time() - tic



# #################################################################################
# # call openMVG_Compute_Matches to filter matches / generate graphs
# if 0:
#     tic = time.time()
#
#     pMatches = subprocess.Popen( [OPENMVG_SFM_BIN + '/openMVG_main_ComputeMatches',
#                                   "-i", path + "/matches/sfm_data.json",
#                                   "-o", path + '/matches',
#                                   "-n", "FASTCASCADEHASHINGL2"
#                                   ] )
#     pMatches.wait()
#     t_matches = time.time() - tic


#################################################################################
# incremental reconstruction without extrinsics
tic = time.time()
if 0:
    reconstruction_dir = path + '/reconstruction_sequential'
    if not os.path.exists(reconstruction_dir):
        os.mkdir(reconstruction_dir)

    pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, 'openMVG_main_IncrementalSfM'),
                                 #'-a', '00000001.png',
                                 #'-b', '00001354.png',
                                 '-i', path + '/matches/sfm_data.json',
                                 '-m', path + '/matches',
                                 '-o', reconstruction_dir,
                                 '-f', 'ADJUST_DISTORTION' # focal length, principal point and distortion should not be adjusted
                                 ] )
    pRecons.wait()
t_incremental = time.time() - tic

#################################################################################
# global reconstruction without extrinsics
if 0:
    tic = time.time()

    reconstruction_dir = path + '/reconstruction_global'
    if not os.path.exists(reconstruction_dir):
        os.mkdir(reconstruction_dir)

    pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, 'openMVG_main_GlobalSfM'),
                                 '-i', path + '/matches/sfm_data.json',
                                 '-m', path + '/matches',
                                 '-o', reconstruction_dir,
                                 '-f', 'ADJUST_DISTORTION' # focal length, principal point and distortion should not be adjusted
                                 ] )
    pRecons.wait()

#################################################################################
# convert .bin to .json

if 0:
    pConv = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, 'openMVG_main_ConvertSfM_DataFormat'),
                                 '-i', reconstruction_dir + '/sfm_data.bin',
                                 '-o', reconstruction_dir + '/sfm_data.json',
                                 ] )
    pConv.wait()


#################################################################################
if 0: # if camera poses from okvis
    execfile('okvisToExtrinsics.py')


#################################################################################
# reconstruction with given extrinsics
if 1:

    reconstruction_dir = path + '/372_488/reconstruction_knownposes'
    if not os.path.exists(reconstruction_dir):
        os.mkdir(reconstruction_dir)

    pPoses = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeStructureFromKnownPoses"),
                                "-f", path + '/matches/matches.f.txt',
                                "-i", path + "/matches/sfm_data.json",
                                "-m", path + '/matches',
                                "-o", os.path.join(reconstruction_dir,"robust.ply")
                                ] )
    pPoses.wait()

#################################################################################
# colorize structure
reconstruction_dir = '/home/rm/Documents/master_thesis/data/okvis_output/reconstruction_sequential'
if 0:

    pColor = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeSfM_DataColor"),
        "-i", reconstruction_dir+"/sfm_data.bin",
        "-o", os.path.join(reconstruction_dir,"colorized.ply")] )
    pColor.wait()

tic = time.time()
if 0: # openMVG_main_openMVG2PMVS -i Dataset/outReconstruction/sfm_data.json -o Dataset/outReconstruction
    pExport = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_openMVG2PMVS"),
        "-i", reconstruction_dir+"/sfm_data.bin",
        "-o", os.path.join(reconstruction_dir,"pmvs_reconstruction")] )
    pExport.wait()
t_MVG2PMVS = time.time() - tic

if 0: # openMVG_main_openMVG2openMVS -i PATH/sfm_data.(json/xml/bin) -d OUTPUT_PATH -o OUTPUT_PATH/Scene
    pExport = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_openMVG2openMVS"),
        "-i", reconstruction_dir+"/sfm_data.bin",
        "-d", os.path.join(reconstruction_dir, "pmvs_reconstruction"),
        "-o", os.path.join(reconstruction_dir,"pmvs_reconstruction/scene")] )
    pExport.wait()




print( "oktomat", t_oktomat)
print( "list", t_list)
print( "incremental reconstruction", t_incremental)
print  "MVG2PMVS", t_MVG2PMVS
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
