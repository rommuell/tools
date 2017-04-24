# -*- coding: utf-8 -*-
import yaml
import io
import matplotlib.pyplot as plt
import sys
import numpy as np
import cv2
from collections import OrderedDict
import os


if len(sys.argv) == 2:
    path = sys.argv[1]
else:
    path = "/home/rm/Documents/master_thesis/data/vicon_leo/bag1/reconstructions/24-04-2017_16:01:45"
    print("WARNING: internal path is used")

path = path + "/time_data.yaml"
print("data source path: " + path)
data=[]
with open(path) as infile:
    for i in range(1):
        _ = infile.readline()
    #data = yaml.load(infile)

    for i in xrange(100):
        ln = yaml.load(infile.readline())
        if ln == None:
            break
        data.append(ln)


labels = []
sizes = []

total_steps = 0.0
for l in data:
    for key in l:
        if key != "total":
            total_steps += l[key]
            labels.append(key)
            sizes.append(l[key])
        elif (l["total"] - total_steps)/l["total"] > 0.01: #other is more than 1%
            labels.append("other")
            sizes.append(l["total"] - total_steps)


# Pie chart, where the slices will be ordered and plotted counter-clockwise:

#explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()

cmap = plt.cm.jet
colors = cmap([0.1, 0.4, 0.7, 1, 0.4, 0.7, 1])
ax1.pie(sizes, labels=labels, pctdistance=0.75,
        shadow=False, startangle=90, autopct='%.1f', colors=colors) #explode=explode, autopct='%1.1f%%',
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()