#!/usr/bin/python
#! -*- encoding: utf-8 -*-

# modified Roman Mueller, 02/2017
import subprocess

command = "/home/rm/code/egm/build/main -i /home/rm/Documents/master_thesis/data/vicon_leo/bag1/okvis_output -c /home/rm/Documents/master_thesis/data/vicon_leo/bag1/config_visensor_mono.yaml -g /home/rm/Documents/master_thesis/data/vicon_leo/bag1/vicon_data_reordered.csv"

command2 = ["/home/rm/code/egm/build/main",
            "-i", "/home/rm/Documents/master_thesis/data/vicon_leo/bag1/okvis_output",
            "-c", "/home/rm/Documents/master_thesis/data/vicon_leo/bag1/config_visensor_mono.yaml",
            "-g", "/home/rm/Documents/master_thesis/data/vicon_leo/bag1/vicon_data_reordered.csv"]

for x in range(0, 6):
    pFeatures = subprocess.Popen(command2)
    pFeatures.wait()
    #comment line in plot_results.py
