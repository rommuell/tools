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



###
# run roscore in terminal seperately
###
bags = []
egms = [] #list containing list of paths to egms files which should be applied to same okvis run
egms_per_ok =[]
directory_0s =[]
poses_gts = []

bags.append("/home/rm/Documents/master_thesis/blender/laborit_away/2/laborit2_away_bl.bag")
directory_0s.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit_away2/l_")
poses_gts.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit_away2/poses.csv")

egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit_away2/egm_0.yaml")
egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit_away2/egm_1.yaml")
egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit_away2/egm_2.yaml")
egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit_away2/egm_3.yaml")
egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit_away2/egm_4.yaml")
egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit_away2/egm_5.yaml")
egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit_away2/egm_6.yaml")
egms.append(egms_per_ok)



bags.append("/home/rm/Documents/master_thesis/blender/laborit/3/laborit3_bl.bag")
directory_0s.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit3/l_")
poses_gts.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit3/poses.csv")

egms_per_ok = []
egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit3/egm_0.yaml")
egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit3/egm_1.yaml")
egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit3/egm_2.yaml")
egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit3/egm_3.yaml")
egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit3/egm_4.yaml")
egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit3/egm_5.yaml")
egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit3/egm_6.yaml")
egms.append(egms_per_ok)



bags.append("/media/rm/9480CE0280CDEB36/experiments_1/quarry7/exp7_cut.bag")
directory_0s.append("/media/rm/9480CE0280CDEB36/experiments_1/quarry7/l_")
poses_gts.append("/media/rm/9480CE0280CDEB36/experiments_1/quarry7/poses.csv")

egms_per_ok = []
egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/quarry7/egm_0.yaml")
egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/quarry7/egm_1.yaml")
egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/quarry7/egm_2.yaml")
egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/quarry7/egm_3.yaml")
egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/quarry7/egm_4.yaml")
egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/quarry7/egm_5.yaml")
egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/quarry7/egm_6.yaml")
egms.append(egms_per_ok)


for e in range(0, bags.__len__()):
    ######################################################
    # set configuration
    # (place bag in a separate folder)

    i_0 = 0
    N = 25
    bag = bags[e]
    directory_0 = directory_0s[e]
    gt = "sim_blender" # set to leica (3D) resp. to vicon or sim or sim_blender (6D)

    #in case of sim_blender
    poses_gt = poses_gts[e]

    #in case of leica 3D ground truth
    bag_leica = "/home/rm/Documents/master_thesis/data/leica_outdoor/31_ST_L_2017-05-05-11-11-38.bag"
    topic = "/leica/position" #ground truth

    #in case of sim
    img_topic = "/firefly/vi_sensor/left/image_raw"
    imu_topic = "/firefly/vi_sensor/imu"

    config = "/home/rm/catkin_ws/src/okvis_ros/okvis/config/config_blender.yaml"
    protocol_template = "/home/rm/Documents/master_thesis/src/tools/protocol.txt"



    for i in xrange(i_0, i_0 + N, 1):
        directory = directory_0 + str(i)

        #######################################################
        if not os.path.exists(directory):
            os.mkdir(directory)

        if gt == "sim":
            dirname = directory #.path.dirname(bag)
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


        #directory = get_parent_dir(bag)

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
            shutil.copy(poses_gt, directory)
            #print("provide ground truth file! (/transform of same bag of which /pose was used for blender input)")
            #raw_input('Press Enter')

            csv_file = directory + "/poses.csv"
            # reorder csv column
            csv_file_reordered = csv_file[:-4] + '_reordered.csv'
            reorder_csv_6D(csv_file, csv_file_reordered)

        # copy config file to bag folder
        shutil.copy(config, directory)
        config = directory +  '/' + os.path.basename(config)

        #run okvis synchronous
        command = "roslaunch okvis_ros okvis_node_synchronous.launch " + "config:=" + config + " bag:=" + bag
        print(command)
        os.system("bash -i -c \"" + command + "\"")
        pyperclip.copy(command)
        #print("paste in terminal and confirm to save (y)")
        #raw_input('Press Enter')
        print
        # pOkvis = subprocess.Popen( ["roslaunch", "okvis_ros", "okvis_node_synchronous.launch",
        #                             "config:=" + config,
        #                             "bag:=" + bag
        #                             ] )
        #pOkvis.wait()

        # move okvis output to bag folder
        shutil.move(okvis_output, directory)

        egm_configs = egms[e]
        for egm_config in egm_configs:

            shutil.copy(egm_config, directory + "/egm.yaml")

            print("Adjust T_VC in egm config file.")
            #raw_input('Press Enter')
            #print

            reconstructions = directory + "/reconstructions"
            if not os.path.exists(reconstructions):
                os.mkdir(reconstructions)

            shutil.copy(protocol_template, reconstructions)

            print("for debugging in qt:")
            command = "/home/rm/code/egm/build/main " + "-i " + directory + "/okvis_output " + "-c " + config + " " + "-g " + csv_file_reordered
            print(command)


            # run egm
            pEval = subprocess.Popen( ["/home/rm/code/egm/build/main",
                                       "-i", directory + "/okvis_output",
                                       "-c", directory +  '/' + os.path.basename(config),
                                       "-g", csv_file_reordered,
                                        ] )
            pEval.wait()
