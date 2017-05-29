import numpy as np
from glob import glob
import os
import matplotlib.pyplot as plt
import math

PI = math.pi

i = 15
N = 2

path = "/home/rm/Documents/master_thesis/data/blender/laborit_away2/l_"

median_reproj_err_ok = []
abs_p_first_ok = []
abs_a_first_ok = []
rms_abs_p_all_ok = []
rms_pos_abs_p_all_scaled_ok = []

median_reproj_err_re = []
abs_p_first_re = []
abs_a_first_re = []
rms_abs_p_all_re = []
rms_pos_abs_p_all_scaled_re = []


median_reproj_err = []
abs_p_first = []
abs_a_first = []
rms_abs_p_all = []
rms_pos_abs_p_all_scaled = []

for x in range(i, i + N):
    path_reopt = glob(path + str(x) + "/reconstructions/" + "*/")[0]

    j = 0
    path_eval = path_reopt + "evaluation" + str(j)
    while (os.path.exists(path_eval)):
        data_ok = np.genfromtxt(path_eval + "/okvis/overview.txt", delimiter=' ', names=True)
        data_re = np.genfromtxt(path_eval + "/reopt/overview.txt", delimiter=' ', names=True)
        data_bla = np.genfromtxt("/home/rm/Documents/master_thesis/data/blender/laborit_away2/l_15/reconstructions/29-05-2017_14:42:26/criteriaList.txt", delimiter=' ', names=True)
        j = j + 1
        path_eval = path_reopt + "evaluation" + str(j)

        median_reproj_err_ok.append(data_ok["median_reproj_err"])
        abs_p_first_ok.append(data_ok["abs_p_first"])
        abs_a_first_ok.append(data_ok["abs_a_first"]*180/PI)
        rms_abs_p_all_ok.append(data_ok["rms_abs_p_all"])
        rms_pos_abs_p_all_scaled_ok.append(data_ok["rms_pos_abs_p_all_scaled"])

        median_reproj_err_re.append(data_re["median_reproj_err"])
        abs_p_first_re.append(data_re["abs_p_first"])
        abs_a_first_re.append(data_re["abs_a_first"]*180/PI)
        rms_abs_p_all_re.append(data_re["rms_abs_p_all"])
        rms_pos_abs_p_all_scaled_re.append(data_re["rms_pos_abs_p_all_scaled"])

        median_reproj_err.append(data_re["median_reproj_err"] / data_ok["median_reproj_err"] * 100)
        abs_p_first.append(data_re["abs_p_first"] / data_ok["abs_p_first"] * 100)
        abs_a_first.append(data_re["abs_a_first"] / data_ok["abs_a_first"] * 100)
        rms_abs_p_all.append(data_re["rms_abs_p_all"] / data_ok["rms_abs_p_all"] * 100)
        rms_pos_abs_p_all_scaled.append(data_re["rms_pos_abs_p_all_scaled"] /data_ok["rms_pos_abs_p_all_scaled"] * 100)


# N = data_ok.dtype.__len__()
# ok_means = (np.mean(median_reproj_err_ok), np.mean(abs_p_first_ok), np.mean(abs_a_first_ok), np.mean(rms_abs_p_all_ok), np.mean(rms_pos_abs_p_all_scaled_ok))
# ok_std = (np.std(median_reproj_err_ok), np.std(abs_p_first_ok), np.std(abs_a_first_ok), np.std(rms_abs_p_all_ok), np.std(rms_pos_abs_p_all_scaled_ok))
#
# ind = np.arange(N) + 0.15 # the x locations for the groups
# width = 0.35       # the width of the bars
#
# fig, ax = plt.subplots()
# rects1 = ax.bar(ind, ok_means, width, color='b', yerr=ok_std, error_kw=dict(ecolor='black'))
#
# re_means = (np.mean(median_reproj_err_re), np.mean(abs_p_first_re), np.mean(abs_a_first_re), np.mean(rms_abs_p_all_re), np.mean(rms_pos_abs_p_all_scaled_re))
# re_std = (np.std(median_reproj_err_re), np.std(abs_p_first_re), np.std(abs_a_first_re), np.std(rms_abs_p_all_re), np.std(rms_pos_abs_p_all_scaled_re))
# rects2 = ax.bar(ind + width, re_means, width, color='r', yerr=re_std, error_kw=dict(ecolor='black'))
#
# # add some text for labels, title and axes ticks
# ax.set_ylabel('Scores')
# ax.set_title('Scores by group and gender')
# ax.set_xticks(ind + width)
# ax.set_xticklabels(('median_reproj_err', 'abs_p_first', 'abs_a_first', 'rms_abs_p_all', 'rms_pos_abs_p_all_scaled'))
#
# ax.legend((rects1[0], rects2[0]), ('OKVIS', 'reopt'))



N = data_ok.dtype.__len__()
means = (np.mean(median_reproj_err), np.mean(abs_p_first), np.mean(abs_a_first), np.mean(rms_abs_p_all), np.mean(rms_pos_abs_p_all_scaled))
std = (np.std(median_reproj_err), np.std(abs_p_first), np.std(abs_a_first), np.std(rms_abs_p_all), np.std(rms_pos_abs_p_all_scaled))

ind = np.arange(N) + 0.2 # the x locations for the groups
width = 0.6       # the width of the bars

fig, ax = plt.subplots()
rects3 = ax.bar(ind, means, width, color='r', yerr=std, error_kw=dict(ecolor='black'))

# add some text for labels, title and axes ticks
ax.set_ylabel('%')
ax.set_title('results of reoptimization relative to OKVIS (window-wise)')
ax.set_xticks(ind + width/2)
ax.set_xticklabels(('median_reproj_err', 'abs_p_first', 'abs_a_first', 'rms_abs_p_all', 'rms_pos_abs_p_all_scaled'))

ax.legend('reopt')
plt.axhline(y=100, xmin=0, xmax=10, linewidth=2, color = 'green')
ylims = ax.get_ylim()
ax.set_ylim((0, ylims[1]))

plt.show()