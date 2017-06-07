#!/usr/bin/python
#! -*- encoding: utf-8 -*-

# modified Roman Mueller, 02/2017
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math
import os
from mpl_toolkits.mplot3d import Axes3D

def ylim_cust(ax):
    ax.grid(True)
    y_lim = np.array(ax.get_ylim())
    y_lim = (y_lim - np.mean(y_lim)) * 1.05 + np.mean(y_lim);
    ax.set_ylim(y_lim)
    ax.set_xlim(0, optWindow.size - 1)
    ax.imshow(optWindow, aspect='auto', extent=(0, optWindow.size, y_lim[0], y_lim[1]), vmax=5, cmap=cm.Greys)
    ax.legend(loc=0)

def filter_outlier(data):
    t = 1000
    data = data[~(data['x'] > t)]
    data = data[~(data['x'] < -t)]
    data = data[~(data['y'] > t)]
    data = data[~(data['y'] < -t)]
    data = data[~(data['z'] > t)]
    data = data[~(data['z'] < -t)]
    data = data[~(data['uncertainty'] > t)]
    return data

PI = math.pi


if len(sys.argv) == 2:
    path = sys.argv[1]
else:
    path = "/media/rm/9480CE0280CDEB36/experiments_1/HG_13/l_2/reconstructions/04-06-2017_16:10:21/evaluation0"
    print("WARNING: internal path is used")

print("data source path: " + path)


fig = plt.figure()

window_data_ok = np.genfromtxt(path + "/okvis/window_data.txt", delimiter=' ', names=True)
window_data_re = np.genfromtxt(path + "/reopt/window_data.txt", delimiter=' ', names=True)
optWindow = np.vstack((window_data_ok["opt_wind"],))
l = optWindow.size
x_space = np.linspace(0, l - 1, num=l)

ax1 = plt.subplot2grid((7,1), (0,0))
plt.subplots_adjust(hspace=0.4, wspace=0.4)
nb = int(np.sum(optWindow))
ax1.set_ylabel('[m]')
ax1.plot(x_space[nb:], window_data_ok["abs_p_all"][nb:], label='OKVIS', color='blue')
ax1.plot(x_space[nb:], window_data_re["abs_p_all"][nb:], label='reopt', color='red')
ax1.set_title('absolute position error overall alignment')
ylim_cust(ax1)

ax2 = plt.subplot2grid((7,1), (1,0))
ax2.set_ylabel('[m]')
ax2.plot(window_data_ok["abs_p_first"], label='OKVIS', color='blue')
ax2.plot(window_data_re["abs_p_first"], label='reopt', color='red')
ax2.set_title('absolute position error alignment of first pose')
ylim_cust(ax2)

ax7 = plt.subplot2grid((7,1), (2,0))
ax7.set_ylabel('[m]')
ax7.plot(x_space[nb:], window_data_ok["abs_p_all_scaled"][nb:], label='OKVIS', color='blue')
ax7.plot(x_space[nb:], window_data_re["abs_p_all_scaled"][nb:], label='reopt', color='red')
ax7.set_title('absolute position error flexible poses alignment including scale')
ylim_cust(ax7)

ax3 = plt.subplot2grid((7,1), (3,0))
ax3.set_ylabel('[deg]')
ax3.plot(window_data_ok["abs_a_all"] * 180 / PI, label='OKVIS', color='blue')
ax3.plot(window_data_re["abs_a_all"] * 180 / PI, label='reopt', color='red')
ax3.set_title('absolute angular error overall alignment')
ylim_cust(ax3)

ax4 = plt.subplot2grid((7,1), (4,0))
ax4.set_ylabel('[deg]')
ax4.plot(window_data_ok["abs_a_first"] * 180 / PI, label='OKVIS', color='blue')
ax4.plot(window_data_re["abs_a_first"] * 180 / PI, label='reopt', color='red')
ax4.set_title('absolute angular error alignment of first pose')
ylim_cust(ax4)

ax5 = plt.subplot2grid((7,1), (5,0))
ax5.set_ylabel('[px]')
ax5.errorbar(x_space, window_data_ok["reproj_mean"], yerr=window_data_ok["reproj_std"], label='OKVIS', color='blue')
ax5.errorbar(x_space, window_data_re["reproj_mean"], yerr=window_data_re["reproj_std"], label='reopt', color='red')
ax5.set_title('reprojection error')
ylim_cust(ax5)
ax5.set_ylim(-0.2, 10)

ax6 = plt.subplot2grid((7,1), (6,0))
ax6.set_ylabel('[-]')
ax6.plot(x_space[1:] - 0.5, window_data_ok["scale"][1:], label='OKVIS', color='blue')
ax6.plot(x_space[1:] - 0.5, window_data_re["scale"][1:], label='reopt', color='red')
ax6.set_title('scale (ratio between gt and reopt kf-kf distance)')
ylim_cust(ax6)

if not os.path.isfile(path + "/okvis/landmarks.txt"):
    plt.show(fig)
    quit()

fig2 = plt.figure()

lm_data_ok = np.genfromtxt(path + "/okvis/landmarks.txt", delimiter=' ', names=True)
lm_data_ok = filter_outlier(lm_data_ok)
lm_data_re = np.genfromtxt(path + "/reopt/landmarks.txt", delimiter=' ', names=True)
lm_data_re = filter_outlier(lm_data_re)

ax = fig2.add_subplot(111, projection='3d')

marker_size = lm_data_ok['uncertainty']#**2
ax.scatter(lm_data_ok['x'], lm_data_ok['y'], lm_data_ok['z'], s=marker_size*60, c='blue')

marker_size = lm_data_re['uncertainty']#**2
ax.scatter(lm_data_re['x'], lm_data_re['y'], lm_data_re['z'], s=marker_size*60,  c='red')
lala = lm_data_re['uncertainty']**2

ax.set_xlim(min(min(lm_data_ok['x']), min(lm_data_re['x'])), max(max(lm_data_ok['x']), max(lm_data_re['x'])))
ax.set_ylim(min(min(lm_data_ok['y']), min(lm_data_re['y'])), max(max(lm_data_ok['y']), max(lm_data_re['y'])))
ax.set_zlim(min(min(lm_data_ok['z']), min(lm_data_re['z'])), max(max(lm_data_ok['z']), max(lm_data_re['z'])))



fig3 = plt.figure()
plt.subplots_adjust(hspace=0.4, wspace=0.4)

reproj_error_ok = np.genfromtxt(path + "/okvis/reprojection_errors.txt", delimiter=' ', names=True)
reproj_error_re = np.genfromtxt(path + "/reopt/reprojection_errors.txt", delimiter=' ', names=True)

if reproj_error_ok.dtype.descr.__len__() <= 20:
    rows = 4
    cols = 5
elif reproj_error_ok.dtype.descr.__len__() <= 30:
    rows = 5
    cols = 6
else:
    rows = 6
    cols = 7

i = 0
for imgs in reproj_error_ok.dtype.descr:
    name = imgs[0]
    r = int(np.floor(i/cols))
    ax = plt.subplot2grid((rows,cols), (r, i - r * cols))
    if name in reproj_error_re.dtype.names:
        ax.hist(reproj_error_re[name], bins=20, range=(0,10), color='red', alpha=0.5)
    ax.hist(reproj_error_ok[name], bins=20, range=(0,10), color='blue', alpha=0.5)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 150)
    ax.set_title(name)
    i = i + 1

plt.show(fig)
plt.show(fig2)


#mng = plt.get_current_fig_manager()
#mng.resize(*mng.window.maxsize())

# comment/uncomment following 2 lines for automatic closing (p. e. when running in a loop)
#plt.show(fig)
#plt.pause(0.1)

#fig.savefig(path + '/results.png', dpi=400 )
print("end of plotting")