#!/usr/bin/python
#! -*- encoding: utf-8 -*-

# modified Roman Mueller, 02/2017
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math

def ylim_cust(ax):
    ax.grid(True)
    y_lim = np.array(ax.get_ylim())
    y_lim = (y_lim - np.mean(y_lim)) * 1.05 + np.mean(y_lim);
    ax.set_ylim(y_lim)
    ax.set_xlim(0, optWindow.size)
    ax.imshow(optWindow, aspect='auto', extent=(0, optWindow.size, y_lim[0], y_lim[1]), vmax=5, cmap=cm.Greys)
    ax.legend()

def twopi_filter(vector):
    PI = math.pi
    for v in np.nditer(vector, op_flags=['readwrite']):
        if v > PI:
            v[...] = v - 2 * PI
        elif v < -PI:
            v[...] = v + 2 * PI
    return vector * 180 / PI


if len(sys.argv) == 2:
    path = sys.argv[1]
else:
    path = "/home/rm/Documents/master_thesis/data/vicon_leo/bag1/reconstructions/14-04-2017_14:05:58"
    print("WARNING: internal path is used")

print("data source path: " + path)

data = np.genfromtxt(path + "/criteriaList.txt", delimiter=' ', names=True)
optWindow = np.vstack((data["reopt1_optWind"],))

fig, axes = plt.subplots(nrows=6, ncols=2)
ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12 = axes.flatten()

ax1.set_ylabel('e_pos [m]')
ax1.plot(data["okvis_e_pos"], label='okvis')
ax1.plot(data['reopt1_e_pos'], label='reoptimized')
ylim_cust(ax1)

ax2.set_ylabel('e_angle [deg]')
ax2.plot(twopi_filter(data['okvis_e_angle']))
ax2.plot(twopi_filter(data['reopt1_e_angle']))
ylim_cust(ax2)


ax3.set_ylabel('e_pos_x [m]')
ax3.plot(data['okvis_e_pos_x'])
ax3.plot(data['reopt1_e_pos_x'])
ylim_cust(ax3)

ax4.set_ylabel('e_angle_yaw [deg]')
ax4.plot(twopi_filter(data['okvis_e_angle_yaw']))
ax4.plot(twopi_filter(data['reopt1_e_angle_yaw']))
ylim_cust(ax4)

ax5.set_ylabel('e_pos_y [m]')
ax5.plot(data['okvis_e_pos_y'])
ax5.plot(data['reopt1_e_pos_y'])
ylim_cust(ax5)

ax6.set_ylabel('e_angle_pitch [deg]')
ax6.plot(twopi_filter(data['okvis_e_angle_pitch']))
ax6.plot(twopi_filter(data['reopt1_e_angle_pitch']))
ylim_cust(ax6)

ax7.set_ylabel('e_pos_z [m]')
ax7.plot(data['okvis_e_pos_z'])
ax7.plot(data['reopt1_e_pos_z'])
ylim_cust(ax7)

ax8.set_ylabel('e_angle_roll [deg]')
ax8.plot(twopi_filter(data['okvis_e_angle_roll']))
ax8.plot(twopi_filter(data['reopt1_e_angle_roll']))
ylim_cust(ax8)

ax9.set_ylabel('')
ax9.plot(data["okvis_e_pos"], label='okvis position error')
ylim_cust(ax9)
ax9b = ax9.twinx()
ax9b.plot(data["A_all_crit"], 'g', label='trace cov matrix')
ax9b.legend(loc=2)
ax9b.set_xlim(0, optWindow.size)

ax10.set_ylabel('')
ax10.plot(data["reoptWindows"], label='reopt windows')
ylim_cust(ax10)
ax10b = ax10.twinx()
ax10b.plot(data["A_all_crit"], 'g', label='trace cov matrix')
ax10b.legend(loc=2)
ax10b.set_xlim(0, optWindow.size)

ax11.set_ylabel('')
ax11.plot(data["okvis_e_pos"], label='okvis position error')
ylim_cust(ax11)
ax11b = ax11.twinx()
ax11b.plot(data["A_pos_crit"], 'g', label='trace pos cov matrix')
ax11b.legend(loc=2)
ax11b.set_xlim(0, optWindow.size)

ax12.set_ylabel('')
ax12.plot(data["okvis_e_angle"], label='okvis angle error')
ylim_cust(ax12)
ax12b = ax12.twinx()
ax12b.plot(data["A_angle_crit"], 'g', label='trace angle cov matrix')
ax12b.legend(loc=2)
ax12b.set_xlim(0, optWindow.size)

mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

plt.show(fig)
fig.savefig(path + '/results.png', dpi=400 )

print("end of plotting")