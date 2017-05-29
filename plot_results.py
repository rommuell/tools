#!/usr/bin/python
#! -*- encoding: utf-8 -*-

# modified Roman Mueller, 02/2017
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math
import os

def ylim_cust(ax):
    ax.grid(True)
    y_lim = np.array(ax.get_ylim())
    y_lim = (y_lim - np.mean(y_lim)) * 1.05 + np.mean(y_lim);
    ax.set_ylim(y_lim)
    ax.set_xlim(0, optWindow.size - 1)
    ax.imshow(optWindow, aspect='auto', extent=(0, optWindow.size, y_lim[0], y_lim[1]), vmax=5, cmap=cm.Greys)
    ax.legend()

PI = math.pi

def twopi_filter(vector):
    for v in np.nditer(vector, op_flags=['readwrite']):
        if v > PI:
            v[...] = v - 2 * PI
        elif v < -PI:
            v[...] = v + 2 * PI
    return vector * 180 / PI

def calc_rms(vec1, vec2):
    i = 0
    acc1 = 0.0
    acc2 = 0.0
    for v1, v2 in zip(vec1, vec2):
        if (v1 != v2) or 0: #peak filter: & ~((v2 - v1) > 0.05)
            acc1 += np.square(v1)
            acc2 += np.square(v2)
            i += 1
    print(i)
    if i > 0:
        return [np.sqrt(acc1 / i), np.sqrt(acc2 / i)]
    else:
        return [0, 0]

def s(val):
    return "%0.5f" % val

def signum(val):
    if val < 0:
        return ""
    else:
        return "+"

if len(sys.argv) == 2:
    path = sys.argv[1]
else:
    path = "/home/rm/Documents/master_thesis/data/blender/exp5/reconstructions/22-05-2017_20:27:44"
    print("WARNING: internal path is used")

print("data source path: " + path)

data = np.genfromtxt(path + "/criteriaList.txt", delimiter=' ', names=True)
optWindow = np.vstack((data["reopt1_optWind"],))

file = open(path + "/readme.txt")
file.readline()
duration = float(file.readline())
file.close()

#fig, axes = plt.subplots(nrows=6, ncols=2)
fig = plt.figure()
#ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12 = axes.flatten()
plt.suptitle(os.path.basename(path) + " (" + "%0.1f" % duration + "s)")

ax1 = plt.subplot2grid((7,2), (0,0))
ax1.set_ylabel('e_pos [m]')
ax1.plot(data["okvis_e_pos"], label='OKVIS')
ax1.plot(data['reopt1_e_pos'], label='reoptimized')
rms = calc_rms(data["okvis_e_pos"], data["reopt1_e_pos"])
ax1.set_title('rms_OKVIS = ' + s(rms[0]) + ", rms_reopt = " + s(rms[1]) + ", delta_rms = " + signum(rms[1] - rms[0]) + s(rms[1] - rms[0]))
ylim_cust(ax1)

ax2 = plt.subplot2grid((7,2), (0,1))
ax2.set_ylabel('e_angle [deg]')
ax2.plot(twopi_filter(data['okvis_e_angle']))
ax2.plot(twopi_filter(data['reopt1_e_angle']))
rms = calc_rms(data["okvis_e_angle"], data["reopt1_e_angle"])
ax2.set_title('rms_OKVIS = ' + s(rms[0]) + ", rms_reopt = " + s(rms[1]) + ", delta_rms = " + signum(rms[1] - rms[0]) + s(rms[1] - rms[0]))
ylim_cust(ax2)

ax3 = plt.subplot2grid((7,2), (1,0))
ax3.set_ylabel('e_pos_x [m]')
ax3.plot(data['okvis_e_pos_x'])
ax3.plot(data['reopt1_e_pos_x'])
ylim_cust(ax3)

ax4 = plt.subplot2grid((7,2), (1,1))
ax4.set_ylabel('e_angle_yaw [deg]')
ax4.plot(twopi_filter(data['okvis_e_angle_yaw']))
ax4.plot(twopi_filter(data['reopt1_e_angle_yaw']))
ylim_cust(ax4)

ax5 = plt.subplot2grid((7,2), (2,0))
ax5.set_ylabel('e_pos_y [m]')
ax5.plot(data['okvis_e_pos_y'])
ax5.plot(data['reopt1_e_pos_y'])
ylim_cust(ax5)

ax6 = plt.subplot2grid((7,2), (2,1))
ax6.set_ylabel('e_angle_pitch [deg]')
ax6.plot(twopi_filter(data['okvis_e_angle_pitch']))
ax6.plot(twopi_filter(data['reopt1_e_angle_pitch']))
ylim_cust(ax6)

ax7 = plt.subplot2grid((7,2), (3,0))
ax7.set_ylabel('e_pos_z [m]')
ax7.plot(data['okvis_e_pos_z'])
ax7.plot(data['reopt1_e_pos_z'])
ylim_cust(ax7)

ax8 = plt.subplot2grid((7,2), (3,1))
ax8.set_ylabel('e_angle_roll [deg]')
ax8.plot(twopi_filter(data['okvis_e_angle_roll']))
ax8.plot(twopi_filter(data['reopt1_e_angle_roll']))
ylim_cust(ax8)

ax9 = plt.subplot2grid((7,2), (4,0))
ax9.set_ylabel('')
ax9.plot(data["okvis_e_pos"], label='OKVIS position error')
ylim_cust(ax9)
ax9b = ax9.twinx()
ax9b.plot(data["A_all_crit"], 'g', label='trace cov matrix')
ax9b.legend(loc=2)
ax9b.set_xlim(0, optWindow.size)

#ax10 = plt.subplot2grid((7,2), (4,1))
#ax10.set_ylabel('')
#ax10.plot(data["reoptWindows"], label='reopt windows')
#ylim_cust(ax10)
#ax10b = ax10.twinx()
#ax10b.plot(data["A_all_crit"], 'g', label='trace cov matrix')
#ax10b.legend(loc=2)
#ax10b.set_xlim(0, optWindow.size)

ax10 = plt.subplot2grid((7,2), (4,1), rowspan=3)
ax10.set_ylabel('')
#ax10.plot(data["okvisIn_e_abs_pos"], label='OKVIS pose(in) abs error')
#ax10.plot(data["okvisMiddle_e_abs_pos"], label='OKVIS pose(middle) abs error', color='black')
ax10.plot(data["okvisOut_e_abs_pos"], label='OKVIS pose abs error')
ax10.plot(data["reopt1_e_abs_pos"], label='reopt pose abs error', color='red')
ylim_cust(ax10)
ax10.legend(loc=0)

#ax11.set_ylabel('')
#ax11.plot(data["okvis_e_pos"], label='OKVIS position error')
#ylim_cust(ax11)
#ax11b = ax11.twinx()
#ax11b.plot(data["A_pos_crit"], 'g', label='trace pos cov matrix')
#ax11b.legend(loc=2)
#ax11b.set_xlim(0, optWindow.size)

ax11 = plt.subplot2grid((7,2), (5,0))
ax11.set_ylabel('')
ax11.plot(data["okvis_e_angle"], label='OKVIS angle error')
ylim_cust(ax11)
ax11b = ax11.twinx()
ax11b.plot(data["A_angle_crit"], 'g', label='trace angle cov matrix')
ax11b.legend(loc=2)
ax11b.set_xlim(0, optWindow.size)

ax13 = plt.subplot2grid((7,2), (6,0))
ax13.set_ylabel('')
ax13.plot(data["okvis_e_pos"], label='OKVIS position error')
ylim_cust(ax13)
ax13b = ax13.twinx()
ax13b.plot(twopi_filter(data["turn_rate"]), 'g', label='turn rate', color='black')
ax13b.legend(loc=2)
ax13b.set_xlim(0, optWindow.size)

mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

# comment/uncomment following 2 lines for automatic closing (p. e. when running in a loop)
#plt.show(fig)
plt.pause(0.1)

fig.savefig(path + '/results.png', dpi=400 )
print("end of plotting")