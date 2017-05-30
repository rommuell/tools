import numpy as np
from glob import glob
import os
import matplotlib.pyplot as plt
import math
import plot_time

PI = math.pi

i = 0
N = 14

path = "/media/rm/9480CE0280CDEB36/experiments_0/laborit_away2_0/l_"

median_reproj_err_ok = []
abs_p_first_ok = []
abs_a_first_ok = []
rms_abs_p_all_ok = []
rms_pos_abs_p_all_scaled_ok = []
scale_overlap = []
scale_flex_ok = []

median_reproj_err_re = []
abs_p_first_re = []
abs_a_first_re = []
rms_abs_p_all_re = []
rms_pos_abs_p_all_scaled_re = []
scale_flex_re = []


median_reproj_err = []
abs_p_first = []
abs_a_first = []
rms_abs_p_all = []
rms_pos_abs_p_all_scaled = []

rec_paths = []
matches_cnt = []

c = 0
for x in range(i, i + N):
    path_reopt = sorted(glob(path + str(x) + "/reconstructions/" + "*/"), key=os.path.getmtime)[0]
    rec_paths.append(path_reopt)

    j = 0

    path_eval = path_reopt + "evaluation" + str(j)
    while (os.path.exists(path_eval)):
        data_ok = np.genfromtxt(path_eval + "/okvis/overview.txt", delimiter=' ', names=True)
        data_re = np.genfromtxt(path_eval + "/reopt/overview.txt", delimiter=' ', names=True)

        median_reproj_err_ok.append(data_ok["median_reproj_err"])
        abs_p_first_ok.append(data_ok["abs_p_first"])
        abs_a_first_ok.append(data_ok["abs_a_first"] * 180 / PI)
        rms_abs_p_all_ok.append(data_ok["rms_abs_p_all"])
        rms_pos_abs_p_all_scaled_ok.append(data_ok["rms_pos_abs_p_all_scaled"])

        median_reproj_err_re.append(data_re["median_reproj_err"])
        abs_p_first_re.append(data_re["abs_p_first"])
        abs_a_first_re.append(data_re["abs_a_first"] * 180 / PI)
        rms_abs_p_all_re.append(data_re["rms_abs_p_all"])
        rms_pos_abs_p_all_scaled_re.append(data_re["rms_pos_abs_p_all_scaled"])

        median_reproj_err.append(data_re["median_reproj_err"] / data_ok["median_reproj_err"] * 100)
        abs_p_first.append(data_re["abs_p_first"] / data_ok["abs_p_first"] * 100)
        abs_a_first.append(data_re["abs_a_first"] / data_ok["abs_a_first"] * 100)
        rms_abs_p_all.append(data_re["rms_abs_p_all"] / data_ok["rms_abs_p_all"] * 100)
        rms_pos_abs_p_all_scaled.append(data_re["rms_pos_abs_p_all_scaled"] /data_ok["rms_pos_abs_p_all_scaled"] * 100)

        data_window_ok = np.genfromtxt(path_eval + "/okvis/window_data.txt", delimiter=' ', names=True)
        data_window_re = np.genfromtxt(path_eval + "/reopt/window_data.txt", delimiter=' ', names=True)
        # number of matches of overlap

        scale_o = []
        scale_fo = []
        scale_fr = []
        for sco, scr, b in zip(data_window_ok["scale"][1:], data_window_re["scale"][1:], data_window_re["opt_wind"][1:]):
            if b:
                scale_o.append(sco)
                if sco != scr:
                    print("what?")
            else:
                scale_fo.append(sco)
                scale_fr.append(scr)
        scale_overlap.append(np.mean(scale_o))
        scale_flex_ok.append(np.mean(scale_fo))
        scale_flex_re.append(np.mean(scale_fr))


        m = []
        for n, b in zip(data_window_re["matchtes"], data_window_re["opt_wind"]):
            if b:
                m.append(n)
        m[:] = [s / sum(m) for s in m]
        matches_cnt.append(m)

        j = j + 1
        c += 1
        path_eval = path_reopt + "evaluation" + str(j)




N = data_ok.dtype.__len__()
ok_means = (np.mean(median_reproj_err_ok), np.mean(abs_p_first_ok), np.mean(abs_a_first_ok), np.mean(rms_abs_p_all_ok), np.mean(rms_pos_abs_p_all_scaled_ok))
ok_std = (np.std(median_reproj_err_ok), np.std(abs_p_first_ok), np.std(abs_a_first_ok), np.std(rms_abs_p_all_ok), np.std(rms_pos_abs_p_all_scaled_ok))

ind = np.arange(N) + 0.15 # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, ok_means, width, color='b', yerr=ok_std, error_kw=dict(ecolor='black'))

re_means = (np.mean(median_reproj_err_re), np.mean(abs_p_first_re), np.mean(abs_a_first_re), np.mean(rms_abs_p_all_re), np.mean(rms_pos_abs_p_all_scaled_re))
re_std = (np.std(median_reproj_err_re), np.std(abs_p_first_re), np.std(abs_a_first_re), np.std(rms_abs_p_all_re), np.std(rms_pos_abs_p_all_scaled_re))
rects2 = ax.bar(ind + width, re_means, width, color='r', yerr=re_std, error_kw=dict(ecolor='black'))

# add some text for labels, title and axes ticks
ax.set_ylabel('units')
ax.set_title('Error of OKVIS vs. reoptimized')
ax.set_xticks(ind + width)
ax.set_xticklabels(('median_reproj_err', 'abs_p_first', 'abs_a_first', 'rms_abs_p_all', 'rms_pos_abs_p_all_scaled'))

ax.legend((rects1[0], rects2[0]), ('OKVIS', 'reopt'))



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

sizes, labels, total_t = plot_time.import_time_data(rec_paths)
sizes[:] = [s / c for s in sizes]
total_t = total_t / c

fig1, ax1 = plt.subplots()
plt.suptitle(os.path.basename(path) + " (" + "%0.1f" % total_t + "s)")

cmap = plt.cm.jet
colors = cmap([0.1, 0.4, 0.7, 1, 0.4, 0.7, 1])
ax1.pie(sizes, labels=labels, pctdistance=0.75, autopct=plot_time.make_autopct(sizes),
        shadow=False, startangle=90, colors=colors)  # explode=explode, autopct='%1.1f%%', autopct='%.1f'
ax1.axis('equal')

length = len(sorted(matches_cnt,key=len, reverse=True)[0])
matches_cnt_mat=np.array([[0]*(length-len(xi)) + xi for xi in matches_cnt])

fig2, ax2 = plt.subplots()
ax2.plot(matches_cnt_mat.T)

fig3, axes = plt.subplots(nrows=1, ncols=3)
ax1, ax2, ax3 = axes.flatten()

ax1.scatter(scale_overlap, scale_flex_ok)
ax1.set_xlabel("scale overlap")
ax1.set_ylabel("scale flex")
ax1.set_title("OKVIS")
ax1.set_xlim((0.7, 1.3))
ax1.set_ylim((0.7, 1.3))
x0,x1 = ax1.get_xlim()
y0,y1 = ax1.get_ylim()
ax1.set_aspect(abs(x1-x0)/abs(y1-y0))

ax2.scatter(scale_overlap, scale_flex_re)
ax2.set_xlabel("scale overlap")
ax2.set_ylabel("scale flex")
ax2.set_title("reopt")
ax2.set_xlim((0.7, 1.3))
ax2.set_ylim((0.7, 1.3))
x0,x1 = ax2.get_xlim()
y0,y1 = ax2.get_ylim()
ax2.set_aspect(abs(x1-x0)/abs(y1-y0))

ax3.scatter(scale_overlap, abs_p_first_re)
ax3.set_xlabel("scale overlap")
ax3.set_ylabel("position error of final kf")
ax3.set_title("reopt")
#ax3.set_xlim((0.7, 1.3))
#ax3.set_ylim((0.7, 1.3))
x0,x1 = ax3.get_xlim()
y0,y1 = ax3.get_ylim()
ax3.set_aspect(abs(x1-x0)/abs(y1-y0))


plt.show()
print