#!/usr/bin/python
#! -*- encoding: utf-8 -*-

# Indicate the openMVG binary directory
OPENMVG_SFM_BIN = "/home/rm/openMVG_Build/Linux-x86_64-Release"

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

output_eval_dir = os.path.join(input_eval_dir, "openMVG_reference")
if not os.path.exists(output_eval_dir):
    os.mkdir(output_eval_dir)

input_dir = input_eval_dir
output_dir = output_eval_dir
print ("Using input dir  : ", input_dir)
print ("      output_dir : ", output_dir)

matches_dir = os.path.join(output_dir, "matches")

# Create the ouput/matches folder if not present
if not os.path.exists(matches_dir):
    os.mkdir(matches_dir)

print ("1. Intrinsics analysis")
pIntrisics = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_SfMInit_ImageListing"),
                               "-i", input_dir,
                                "-o", matches_dir,
                                "-c", "5", # c camera model
                                "-f", "463.608"] )

pIntrisics.wait()

print ("2. Compute features")
pFeatures = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeFeatures"),
                               "-i", matches_dir+"/sfm_data.json",
                               "-o", matches_dir,
                               "-m", "SIFT",
                               "-f", "1",
                               "-n", "8"  # -n number of threads
                               ] )

pFeatures.wait()

print ("3. Compute matches")
pMatches = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeMatches"),
                              "-i", matches_dir+"/sfm_data.json",
                              "-o", matches_dir,
                              "-f", "1",
                              "-n", "FASTCASCADEHASHINGL2",
                              #"-v", "8"
                              ] )
pMatches.wait()

reconstruction_dir = os.path.join(output_dir,"reconstruction_sequential")
print ("4. Do Incremental/Sequential reconstruction") #set manually the initial pair to avoid the prompt question
pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_IncrementalSfM"),
                             "-i", matches_dir+"/sfm_data.json",
                             "-m", matches_dir,
                             "-o", reconstruction_dir
                             ])
pRecons.wait()

print ("5. Colorize Structure")
pColor = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeSfM_DataColor"),
                             "-i", reconstruction_dir+"/sfm_data.bin",
                             "-o", os.path.join(reconstruction_dir,"colorized.ply")
                             ] )
pColor.wait()

print ("6. Structure from Known Poses (robust triangulation)")
pRobust = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeStructureFromKnownPoses"),
                             "-i", reconstruction_dir+"/sfm_data.bin",
                             "-m", matches_dir,
                             "-o", os.path.join(reconstruction_dir,"robust.ply")
                             ] )
pRobust.wait()