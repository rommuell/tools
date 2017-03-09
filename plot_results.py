#!/usr/bin/python
#! -*- encoding: utf-8 -*-

# modified Roman Mueller, 02/2017
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def ylim_cust(ax):
    ax.grid(True)
    y_lim = np.array(ax.get_ylim())
    y_lim = (y_lim - np.mean(y_lim)) * 1.05 + np.mean(y_lim);
    ax.set_ylim(y_lim)
    ax.set_xlim(0, optWindow.size)
    ax.imshow(optWindow, aspect='auto', extent=(0, optWindow.size, y_lim[0], y_lim[1]), vmax=5, cmap=cm.Greys)
    ax.legend()

if len(sys.argv) == 2:
    path = sys.argv[1]
else:
    path = "/home/rm/Documents/master_thesis/data/vicon/wall_circ/reconstructions/07-03-2017_17:50:00"
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

ax2.set_ylabel('e_angle [rad]')
ax2.plot(data['okvis_e_angle'])
ax2.plot(data['reopt1_e_angle'])
ylim_cust(ax2)


ax3.set_ylabel('e_pos_x [m]')
ax3.plot(data['okvis_e_pos_x'])
ax3.plot(data['reopt1_e_pos_x'])
ylim_cust(ax3)

ax4.set_ylabel('e_angle_yaw [rad]')
ax4.plot(data['okvis_e_angle_yaw'])
ax4.plot(data['reopt1_e_angle_yaw'])
ylim_cust(ax4)

ax5.set_ylabel('e_pos_y [m]')
ax5.plot(data['okvis_e_pos_y'])
ax5.plot(data['reopt1_e_pos_y'])
ylim_cust(ax5)

ax6.set_ylabel('e_angle_pitch [rad]')
ax6.plot(data['okvis_e_angle_pitch'])
ax6.plot(data['reopt1_e_angle_pitch'])
ylim_cust(ax6)

ax7.set_ylabel('e_pos_z [m]')
ax7.plot(data['okvis_e_pos_z'])
ax7.plot(data['reopt1_e_pos_z'])
ylim_cust(ax7)

ax8.set_ylabel('e_angle_roll [rad]')
ax8.plot(data['okvis_e_angle_roll'])
ax8.plot(data['reopt1_e_angle_roll'])
ylim_cust(ax8)

ax9.set_ylabel('')
ax9.plot(data["okvis_e_pos"], label='okvis position error')
ylim_cust(ax9)
ax9b = ax9.twinx()
ax9b.plot(data["A_all_crit"], 'g', label='trace cov matrix')
ax9b.legend(loc=2)

mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

plt.show(fig)
fig.savefig(path + '/results.png', dpi=400 )

print("end of plotting")