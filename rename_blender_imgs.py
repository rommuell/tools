import numpy as np
import os
import csv

directory = "/home/rm/Documents/master_thesis/blender/laborit_away/2"
# images in directory/cam0
# poses.csv (from rosbag: rostopic echo -b poses.bag -p /firefly/vi_sensor/ground_truth/pose >poses.csv)
# imu.csv (from rosbag: rostopic echo -b poses.bag -p /firefly/vi_sensor/imu >imu.csv)
if 1:
    # renaming imgs
    data = np.genfromtxt(directory + "/poses.csv", delimiter=',', names=True)
    img_list = os.listdir(directory + "/cam0")
    #img_list.sort()
    #img_list = sorted(img_list, key = lambda x: int(x.split(".")[0]))
    img_list = sorted(img_list, key = lambda x: int(x.split(".")[0][5:])) #in case of prename Image (Image0001.png)


    i = 0;
    j = 0;
    for time in data["time"]:
        filename = img_list[j]
        filename_t = filename[:-4]
        #i_filename = int(filename_t)
        i_filename = int(filename_t[5:]) #in case of prename Image (Image0001.png)
        if (i + 1 == i_filename):
            os.rename(directory +"/cam0/" + filename, directory +"/cam0/" + str(int(time)) + ".png")
            j += 1
            if (j >= img_list.__len__()):
                break
        i += 1

#creating imu0.csv with imu data
with open(directory + "/imu.csv", 'rb') as inFile, open(directory + "/imu0.csv", 'wb') as outFile:
    fieldnames = ['field.header.stamp', 'field.angular_velocity.x', 'field.angular_velocity.y',
                  'field.angular_velocity.z',
                  'field.linear_acceleration.x', 'field.linear_acceleration.y', 'field.linear_acceleration.z']
    writer = csv.DictWriter(outFile, fieldnames=fieldnames, extrasaction='ignore')
#  writer.writerow(['timestamp,omega_x,omega_y,omega_z,alpha_x,alpha_y,alpha_z'])
    writer.writerow({'field.header.stamp': 'timestamp', 'field.angular_velocity.x': 'omega_x', 'field.angular_velocity.y': 'omega_y', 'field.angular_velocity.z': 'omega_z',
                    'field.linear_acceleration.x': 'alpha_x', 'field.linear_acceleration.y': 'alpha_y', 'field.linear_acceleration.z': 'alpha_z'})

    r = csv.reader(inFile)

    for row in csv.DictReader(inFile):
        # writes the reordered rows to the new file
        writer.writerow(row)
