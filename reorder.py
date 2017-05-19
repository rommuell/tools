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

def reorder_csv_3D(filename_in, filename_out):
    with open(filename_in, 'r') as infile, open(filename_out, 'a') as outfile:

        # output dict needs a list for new column ordering
        fieldnames = ['field.header.stamp', 'field.point.x', 'field.point.y',
                      'field.point.z',
                      '%time', 'field.header.seq', 'field.header.frame_id']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        # reorder the header first
        writer.writeheader()
        for row in csv.DictReader(infile):
            # writes the reordered rows to the new file
            writer.writerow(row)

def reorder_csv_6D(filename_in, filename_out):
    with open(filename_in, 'r') as infile, open(filename_out, 'a') as outfile:

        # output dict needs a list for new column ordering
        fieldnames = ['field.header.stamp', 'field.transform.translation.x', 'field.transform.translation.y',
                      'field.transform.translation.z',
                      'field.transform.rotation.x', 'field.transform.rotation.y', 'field.transform.rotation.z',
                      'field.transform.rotation.w',
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

bag = "/home/rm/Documents/master_thesis/data/blender/exp5_1/exp5.bag"
gt = "sim_blender" # set to leica (3D) resp. to vicon or sim or sim_blender (6D)
bag_leica = "/home/rm/Documents/master_thesis/data/leica_outdoor/31_ST_L_2017-05-05-11-11-38.bag"
topic = "/leica/position" #ground truth

#in case of sim
img_topic = "/firefly/vi_sensor/left/image_raw"
imu_topic = "/firefly/vi_sensor/imu"

config = "/home/rm/catkin_ws/src/okvis_ros/okvis/config/config_blender.yaml"
egm_config = "/home/rm/Documents/master_thesis/src/tools/egm.yaml"
protocol_template = "/home/rm/Documents/master_thesis/src/tools/protocol.txt"

#######################################################
if gt == "sim":
    dirname = os.path.dirname(bag)
    command = "rosrun rosbag topic_renamer.py " + img_topic + " " + bag + " /cam0/image_raw " + dirname + "/temp.bag"
    command += " && rosrun rosbag topic_renamer.py " + imu_topic + " "+ dirname + "/temp.bag" + " /imu0 " + dirname + "/sim.bag"
    command += " && rm " + dirname + "/temp.bag && rm " + bag
    bag = dirname + "/sim.bag"
    print(command)
    pyperclip.copy(command)
    print("paste in terminal")
    raw_input('Press Enter')
    print

okvis_output = "/home/rm/Documents/master_thesis/data/okvis_output"
if not os.path.exists(okvis_output):
    os.mkdir(okvis_output)
else:
    sys.exit("okvis_output already exists")


directory = get_parent_dir(bag)

# ground truth bag to csv
if gt == "vicon" or gt == "sim":
    csv_file = directory + "/vicon_data.csv"

    command = "rostopic echo " + "-b " + bag + " -p " +  topic + " >" + csv_file
    print(command)
    pyperclip.copy(command)
    print("paste in terminal")
    raw_input('Press Enter')
    print

    # reorder csv column
    csv_file_reordered = csv_file[:-4] + '_reordered.csv'
    reorder_csv_6D(csv_file, csv_file_reordered)

elif gt == "leica":
    csv_file = directory + "/leica_data.csv"

    command = "rostopic echo " + "-b " + bag_leica + " -p " + topic + " >" + csv_file
    print(command)
    pyperclip.copy(command)
    print("paste in terminal")
    raw_input('Press Enter')
    print

    # reorder csv column
    csv_file_reordered = csv_file[:-4] + '_reordered.csv'
    reorder_csv_3D(csv_file, csv_file_reordered)
elif gt =='sim_blender':
    print("provide ground truth file!")
    raw_input('Press Enter')

    csv_file = directory + "/poses.csv"
    # reorder csv column
    csv_file_reordered = csv_file[:-4] + '_reordered.csv'
    reorder_csv_6D(csv_file, csv_file_reordered)

# copy config file to bag folder
shutil.copy(config, directory)

#run okvis synchronous
command = "roslaunch okvis_ros okvis_node_synchronous.launch " + "config:=" + config + " bag:=" + bag
print(command)
pyperclip.copy(command)
print("paste in terminal and confirm to save (y)")
raw_input('Press Enter')
print
# pOkvis = subprocess.Popen( ["roslaunch", "okvis_ros", "okvis_node_synchronous.launch",
#                             "config:=" + config,
#                             "bag:=" + bag
#                             ] )
#pOkvis.wait()

# move okvis output to bag folder
shutil.move(okvis_output, directory)
shutil.copy(egm_config, directory)

print("Adjust T_VC in egm config file.")
raw_input('Press Enter')
print

reconstructions = directory + "/reconstructions"
if not os.path.exists(reconstructions):
    os.mkdir(reconstructions)

shutil.copy(protocol_template, reconstructions)

print("for debugging in qt:")
command = "/home/rm/code/egm/build/main " + "-i " + directory + "/okvis_output " + "-c " + directory +  '/' + os.path.basename(config) + " " + "-g " + csv_file_reordered
print(command)


# run okvis synchronous
pEval = subprocess.Popen( ["/home/rm/code/egm/build/main",
                           "-i", directory + "/okvis_output",
                           "-c", directory +  '/' + os.path.basename(config),
                           "-g", csv_file_reordered,
                            ] )
pEval.wait()
