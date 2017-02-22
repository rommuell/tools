#!/usr/bin/python
#! -*- encoding: utf-8 -*-

# modified Roman Mueller, 02/2017
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.cm as cm


#path = sys.argv[1]
path = "/home/rm/Documents/master_thesis/data/vicon/wall_circ/reconstructions/22-02-2017_10:36:36"

data = np.genfromtxt(path + "/criteriaList.txt", delimiter=' ', names=True)
optWindow = np.vstack((data["reopt1_optWind"],))

fig, axes = plt.subplots(nrows=6, ncols=2)
ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12 = axes.flatten()

ax1.set_ylabel('e_pos [m]')
ax1.imshow(optWindow, aspect='auto', vmax= 5, cmap=cm.Greys)
ax1.plot(data["okvis_e_pos"])
ax1.plot(data['reopt1_e_pos'])
ax1.grid(True)


#ax9b = ax9.twinx()
#ax9b.plot(data["reopt1_optWind"])

ax2.set_ylabel('e_angle []')
ax2.plot(data['okvis_e_angle'])
ax2.plot(data['reopt1_e_angle'])
ax2.grid(True)
ax2.imshow(optWindow, aspect='auto', vmax= 5, cmap=cm.Greys)

ax3.set_ylabel('e_pos_x [m]')
ax3.plot(data['okvis_e_pos_x'])
ax3.plot(data['reopt1_e_pos_x'])
ax3.grid(True)
ax3.imshow(optWindow, aspect='auto', vmax= 5, cmap=cm.Greys) #extent=(0, 150, min(data['reopt1_optWind']), max(data['reopt1_optWind'])),

ax4.set_ylabel('e_angle_yaw []')
ax4.plot(data['okvis_e_angle_yaw'])
ax4.plot(data['reopt1_e_angle_yaw'])
ax4.grid(True)
ax4.imshow(optWindow, aspect='auto', vmax= 5, cmap=cm.Greys)

ax5.set_ylabel('e_pos_y [m]')
ax5.plot(data['okvis_e_pos_y'])
ax5.plot(data['reopt1_e_pos_y'])
ax5.grid(True)
ax5.imshow(optWindow, aspect='auto', vmax= 5, cmap=cm.Greys)

ax6.set_ylabel('e_angle_pitch []')
ax6.plot(data['okvis_e_angle_pitch'])
ax6.plot(data['reopt1_e_angle_pitch'])
ax6.grid(True)
ax6.imshow(optWindow, aspect='auto', vmax= 5, cmap=cm.Greys)

ax7.set_ylabel('e_pos_z [m]')
ax7.plot(data['okvis_e_pos_z'])
ax7.plot(data['reopt1_e_pos_z'])
ax7.grid(True)
ax7.imshow(optWindow, aspect='auto', vmax= 5, cmap=cm.Greys)

ax8.set_ylabel('e_angle_roll []')
ax8.plot(data['okvis_e_angle_roll'])
ax8.plot(data['reopt1_e_angle_roll'])
ax8.grid(True)
ax8.imshow(optWindow, aspect='auto', vmax= 5, cmap=cm.Greys)

mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())

plt.show(fig)
fig.savefig(path + '/results.png', dpi=400 )

print("H")