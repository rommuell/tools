import numpy as np
import os
import csv

directory = "/home/rm/Documents/master_thesis/blender/imgs5"
# images in directory/depth
# poses.csv (from rosbag: rostopic echo -b poses.bag -p /firefly/vi_sensor/ground_truth/pose >poses.csv)


# renaming imgs
data = np.genfromtxt(directory + "/poses.csv", delimiter=',', names=True)
img_list = os.listdir(directory + "/depth")
#img_list.sort()
img_list = sorted(img_list, key = lambda x: int(x.split(".")[0]))

i = 0;
j = 0;
for time in data["time"]:
    filename = img_list[j]
    filename_t = filename[:-4]
    i_filename = int(filename_t)
    if (i + 1 == i_filename):
        os.rename(directory +"/depth/" + filename, directory +"/depth/" + str(int(time)) + ".exr")
        j += 1
        if (j >= img_list.__len__()):
            break
    i += 1