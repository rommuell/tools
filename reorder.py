#!/usr/bin/python
#! -*- encoding: utf-8 -*-

# modified Roman Mueller, 25/01/2017

import csv
import os
import subprocess
import shutil
import sys
import pyperclip

def get_parent_dir(directory):
    return os.path.dirname(directory)

def reorder_csv(filename_in, filename_out):
    with open(filename_in, 'r') as infile, open(filename_out, 'a') as outfile:

        # output dict needs a list for new column ordering
        fieldnames = ['field.header.stamp', 'field.transform.translation.x', 'field.transform.translation.y',
                      'field.transform.translation.z',
                      'field.transform.rotation.w', 'field.transform.rotation.x', 'field.transform.rotation.y',
                      'field.transform.rotation.z',
                      'field.child_frame_id', '%time', 'field.header.seq', 'field.header.frame_id']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        # reorder the header first
        writer.writeheader()
        for row in csv.DictReader(infile):
            # writes the reordered rows to the new file
            writer.writerow(row)


######################################################
# set configuration
# (place bag in a separate folder)

bag = "/home/rm/Documents/master_thesis/data/vicon/v1/2017-01-26-17-45-35.bag"
topic = "/camera_imu/vrpn_client/estimated_transform"
config = "/home/rm/catkin_ws/src/okvis_ros/okvis/config/config_visensor_mono.yaml"

#######################################################

okvis_output = "/home/rm/Documents/master_thesis/data/okvis_output"
if not os.path.exists(okvis_output):
    os.mkdir(okvis_output)
else:
    sys.exit("okvis_output already exists")


directory = get_parent_dir(bag)


# bag to csv
csv_file = directory + "/vicon_data.csv"

command = "rostopic echo " + "-b " + bag + " -p " +  topic + " >" + csv_file
print(command)
pyperclip.copy(command)
print("paste in terminal")
raw_input('Press Enter')
print

#pBagToCsv = subprocess.Popen( ["rostopic", "echo",
#                               "-b", bag,
#                               "-p",  topic,
#                               ">", csv_file,
#                               ])
#pBagToCsv.wait()

# reorder csv column
csv_file_reordered = csv_file[:-4] + '_reordered.csv'
reorder_csv(csv_file, csv_file_reordered)

# copy donfig file to bag folder
shutil.copy(config, directory)

#run okvis synchronous
command = "roslaunch okvis_ros okvis_node_synchronous.launch " + "config:=" + config + " bag:=" + bag
print(command)
pyperclip.copy(command)
print("paste in terminal")
raw_input('Press Enter')
print
# pOkvis = subprocess.Popen( ["roslaunch", "okvis_ros", "okvis_node_synchronous.launch",
#                             "config:=" + config,
#                             "bag:=" + bag
#                             ] )
#pOkvis.wait()

# move okvis output to bag folder
shutil.move(okvis_output, directory)


# run okvis synchronous
pEval = subprocess.Popen( ["/home/rm/egm/build/main",
                           "-i", directory + "/okvis_output",
                           "-c", config,
                           "-g", csv_file_reordered,
                            ] )
pEval.wait()






# roslaunch okvis_ros okvis_node_synchronous.launch config:=/home/rm/catkin_ws/src/okvis_ros/okvis/config/config_visensor_mono.yaml bag:=/home/rm/Documents/master_thesis/data/marco/ToF_d1_5Hz.bag