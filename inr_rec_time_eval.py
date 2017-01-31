#!/usr/bin/python
#! -*- encoding: utf-8 -*-

# Python script to launch OpenMVG SfM tools on an image dataset
#
# usage : python img_wo_geotag.py
# SfM from non-geotagged images
# modified Roman Mueller, 06/11/2016

# Indicate the openMVG binary directory
OPENMVG_SFM_BIN = "/home/rm/openMVG_Build/Linux-x86_64-RELEASE"

import os
import subprocess
import time
import numpy as np

Iter = 30
vert = np.empty(Iter)
t_rec = np.empty(Iter)

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

matches_dir = "/home/rm/Documents/master_thesis/data/aerial_bags/aerial1_cutted/output_t13/matches"

for i in range(0, Iter):
	reconstruction_dir = "/home/rm/Documents/master_thesis/data/aerial_bags/aerial1_cutted/rec_inc_eval_o13/" + str(i)
	print ("3. Do Incremental/Sequential reconstruction") #set manually the initial pair to avoid the prompt question

	tic = time.time()
	pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_IncrementalSfM"),  
		"-P",
		"-i", matches_dir+"/sfm_data.json", 
		"-m", matches_dir, 
		"-o", reconstruction_dir] )
	pRecons.wait()
	t_rec[i] = time.time() - tic

	print ("5. Colorize Structure")
	pRecons = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_ComputeSfM_DataColor"), 
		"-i", reconstruction_dir+"/sfm_data.bin", 
		"-o", os.path.join(reconstruction_dir,"colorized.ply")] )
	pRecons.wait()
	vert[i] = file_len(reconstruction_dir + "/colorized.ply")


print( "rec", t_rec)
print( "col", vert)
