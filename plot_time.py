# -*- coding: utf-8 -*-
import yaml
import io
import matplotlib.pyplot as plt
import sys
import numpy as np
import cv2
from collections import OrderedDict
import os

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = pct*total/100.0
        return '{p:.0f}%  ({v:.1f})'.format(p=pct,v=val)
    return my_autopct


if len(sys.argv) == 2:
    path = sys.argv[1]
else:
    path = "/home/rm/Documents/master_thesis/data/vicon_leo/bag1/reconstructions/25-04-2017_18:26:30"
    print("WARNING: internal path is used")

print("data source path: " + path + "/time_data.yaml")
data=[]
with open(path + "/time_data.yaml") as infile:
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

total_time = 0.0
total_steps = 0.0
for l in data:
    for key in l:
        if key != "total":
            total_steps += l[key]
            labels.append(key)
            sizes.append(l[key])
        else:
            total_time = l["total"]
            t_other = l["total"] - total_steps
            print("t_other: " + str(t_other))
            if t_other/l["total"] > 0.01: #other is more than 1%
                labels.append("other")
                sizes.append(l["total"] - total_steps)


# Pie chart, where the slices will be ordered and plotted counter-clockwise:

#explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
plt.suptitle(os.path.basename(path) + " (" + "%0.1f" % total_time + "s)")

cmap = plt.cm.jet
colors = cmap([0.1, 0.4, 0.7, 1, 0.4, 0.7, 1])
ax1.pie(sizes, labels=labels, pctdistance=0.75, autopct=make_autopct(sizes),
        shadow=False, startangle=90, colors=colors) #explode=explode, autopct='%1.1f%%', autopct='%.1f'
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

plt.show()
plt.pause(0.1)
fig1.savefig(path + "/time.png", dpi=400 )