# -*- coding: utf-8 -*-
import yaml
import io
import matplotlib.pyplot as plt
import sys
import numpy as np
import cv2
from collections import OrderedDict
import os

def import_time_data(paths):
    data=[]

    for path in paths:
        file = path + "/time_data.yaml"

        if not os.path.exists(file):
            print "time_data.yaml not found"
            continue

        with open(file) as infile:
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
                #print("t_other: " + str(t_other))
                #if t_other/l["total"] > 0.01: #other is more than 1%
                #    labels.append("other")
                #    sizes.append(l["total"] - total_steps)


    # Pie chart, where the slices will be ordered and plotted counter-clockwise:

    #explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    if True: #if True, sum up over windows

        f = m = b = t = 0.0
        labels2 = labels
        sizes2 = sizes
        labels = []
        sizes = []
        for l, s in zip(labels2, sizes2):
            spl = l.split("_")[-1]
            if spl == "Features":
                f += s
            elif spl == "Matches":
                m += s
            elif spl == "Reconstruction":
                b += s
            elif spl == "threshold":
                t += s
            else:
                sizes.append(s)
                labels.append(l)
        sizes.append(t)
        labels.append("Criterion Evaluation")
        sizes.append(f)
        labels.append("Compute Features")
        sizes.append(m)
        labels.append("Compute Matches")
        sizes.append(b)
        labels.append("Global Reconstruction")
    return sizes, labels, total_steps

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = pct*total/100.0
        return '{p:.0f}%  ({v:.1f})'.format(p=pct,v=val)
    return my_autopct

if __name__ == "__main__":
    if len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        path = "/home/rm/Documents/master_thesis/data/blender/laborit_away2/l_16/reconstructions/29-05-2017_15:27:51"
        print("WARNING: internal path is used")

    print("data source path: " + path + "/time_data.yaml")
    paths = []
    paths.append(path)
    sizes, labels, total_t = import_time_data(paths)

    fig1, ax1 = plt.subplots()
    plt.suptitle(os.path.basename(path) + " (" + "%0.1f" % total_t + "s)")

    cmap = plt.cm.jet
    colors = cmap([0.1, 0.4, 0.7, 1, 0.4, 0.7, 1])
    ax1.pie(sizes, labels=labels, pctdistance=0.75, autopct=make_autopct(sizes),
            shadow=False, startangle=90, colors=colors) #explode=explode, autopct='%1.1f%%', autopct='%.1f'
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())

    #plt.show()
    plt.pause(0.1)
    fig1.savefig(path + "/time.png", dpi=400 )