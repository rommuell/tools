#!/usr/bin/python
#! -*- encoding: utf-8 -*-

# Python script to launch OpenMVG SfM tools on an image dataset
#
# usage : python img_wo_geotag.py
# SfM from non-geotagged images
# modified Roman Mueller, 06/11/2016

# Indicate the openMVG binary directory
OPENMVG_SFM_BIN = "/home/rm/openMVG_Build/Linux-x86_64-RELEASE"

# Indicate the openMVG camera sensor width directory
CAMERA_SENSOR_WIDTH_DIRECTORY = "/home/rm/openMVG/src/software/SfM" + "/../../openMVG/exif/sensor_width_database"

import commands
import os
import subprocess
import sys
import time

def get_parent_dir(directory):
    import os
    return os.path.dirname(directory)

input_eval_dir = "/home/rm/Documents/master_thesis/data/okvis_output"
# Checkout an OpenMVG image dataset with Git
if not os.path.exists(input_eval_dir):
	sys.exit("Input directory does not exist!")

output_eval_dir = os.path.join(input_eval_dir, "openMVG_pure")
if not os.path.exists(output_eval_dir):
  os.mkdir(output_eval_dir)

input_dir = input_eval_dir
output_dir = output_eval_dir
print ("Using input dir  : ", input_dir)
print ("      output_dir : ", output_dir)

matches_dir = os.path.join(output_dir, "matches")
camera_file_params = os.path.join(CAMERA_SENSOR_WIDTH_DIRECTORY, "sensor_width_camera_database.txt")


# Create the ouput/matches folder if not present
if not os.path.exists(matches_dir):
  os.mkdir(matches_dir)

# tic = time.time()
# print ("1. Intrinsics analysis")
# pIntrisics = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_SfMInit_ImageListing"),
#   #"-P",
#   "-i", input_dir,
#   "-o", matches_dir,
#   "-d", camera_file_params,
#   "-c", "1", # c camera model
#   "-f", "902"] )
#
# pIntrisics.wait()
# t_intrinsic = time.time()- tic

tic = time.time()
print ("2. Compute features")
pFeatures = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeFeatures"),
  "-i", matches_dir+"/sfm_data.json", 
  "-o", matches_dir, 
  "-m", "SIFT", 
  "-f", "1",
  "-n", "8"  # -n number of threads
  ] )

pFeatures.wait()
t_features = time.time() - tic

tic = time.time()
print ("2. Compute matches")
pMatches = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeMatches"),
  "-i", matches_dir+"/sfm_data.json", 
  "-o", matches_dir, 
  "-f", "1", 
  "-n", "FASTCASCADEHASHINGL2",
  "-v", "12"
  ] )
pMatches.wait()
t_matches = time.time() - tic

tic = time.time()
reconstruction_dir = os.path.join(output_dir,"reconstruction_sequential")
print ("3. Do Incremental/Sequential reconstruction") #set manually the initial pair to avoid the prompt question

pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_IncrementalSfM"),  
	#"-P",
	"-i", matches_dir+"/sfm_data.json", 
	"-m", matches_dir, 
	"-o", reconstruction_dir,
    '-f', 'NONE'
    ] )

pRecons.wait()
t_reconstruction = time.time() - tic

tic = time.time()
print ("5. Colorize Structure")
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeSfM_DataColor"), 
	"-i", reconstruction_dir+"/sfm_data.bin", 
	"-o", os.path.join(reconstruction_dir,"colorized.ply")] )
pRecons.wait()
t_colorize = time.time() - tic

#print( "Intrinsic", t_intrinsic)
print( "Features", t_features)
print( "Matches", t_matches)
print( "Inc. reconstruction", t_reconstruction)
print( "Colorize", t_colorize)
print( "total time:", t_features + t_matches + t_reconstruction + t_colorize)

#print ("4. Structure from Known Poses (robust triangulation)")
#pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeStructureFromKnownPoses"),  "-i", reconstruction_dir+"/sfm_data.bin", "-m", matches_dir, "-o", os.path.join(reconstruction_dir,"robust.ply")] )
#pRecons.wait()
