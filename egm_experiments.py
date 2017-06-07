import numpy as np
from glob import glob
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import math
import plot_time
from sklearn import linear_model, datasets


def multipage(filename, figs=None, dpi=200):
    pp = PdfPages(filename)
    if figs is None:
        figs = [plt.figure(n) for n in plt.get_fignums()]
    for fig in figs:
        fig.savefig(pp, format='pdf')
    pp.close()

def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        if not np.isnan(height):
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%1.1f' % height,
                    ha='center', va='bottom')

PI = math.pi

i = 0
N = 25
R_0 = 0
R_1 = 0
#path = "/media/rm/9480CE0280CDEB36/experiments_1/quarry7"
#path = "/media/rm/9480CE0280CDEB36/experiments_1/laborit_away2"
path = "/media/rm/9480CE0280CDEB36/experiments_1/laborit3"
#path = "/media/rm/9480CE0280CDEB36/experiments_1/HG_13"

#path = "/media/rm/9480CE0280CDEB36/experiments_2/23_CAB"
#path = "/media/rm/9480CE0280CDEB36/experiments_2/24_CAB"
#path = "/media/rm/9480CE0280CDEB36/experiments_2/31_ST"

path = path + "/l_"

for R in range(R_0, R_1 + 1):
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
    abs_p_last = []
    abs_a_last = []

    rec_paths = []
    matches_cnt = []

    c = 0 #number of windows
    k = 0 #number of keyframes that are reoptimized
    k_tot = 0 #number of keyframes including fist and second overlap
    for x in range(i, i + N):
        rec_path = path + str(x) + "/reconstructions/"

        if not os.path.exists(rec_path):
            print "this reconstruction directory does not exist (i to N might be out of range)"
            continue

        fl = sorted(glob(rec_path + "*/"), key=os.path.getmtime)
        print R, x
        path_reopt = fl[R]
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

            med = data_re["median_reproj_err"] / data_ok["median_reproj_err"] * 100
            if not np.isnan(med):
                median_reproj_err.append(med)
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
                        print("scale of overlap are not identical, should not happen (T_CP_?)! ratio = ", sco / scr)
                else:
                    scale_fo.append(sco)
                    scale_fr.append(scr)
            scale_overlap.append(np.mean(scale_o))
            scale_flex_ok.append(np.mean(scale_fo))
            scale_flex_re.append(np.mean(scale_fr))

            # set iterator to last in overlap
            it = 0;
            while data_window_ok["opt_wind"][it]:
                it += 1
            it -= 1
            abs_p_last.append( (data_window_re["abs_p_first"][-1] - data_window_re["abs_p_first"][it]) / (data_window_ok["abs_p_first"][-1] - data_window_re["abs_p_first"][it]))
            abs_a_last.append( (data_window_re["abs_a_first"][-1] - data_window_re["abs_a_first"][it]) / (data_window_ok["abs_a_first"][-1] - data_window_re["abs_a_first"][it]))

            m = []
            for n, b in zip(data_window_re["matchtes"], data_window_re["opt_wind"]):
                if b:
                    m.append(n)
            m[:] = [s / sum(m) for s in m]
            matches_cnt.append(m)

            j = j + 1
            c += 1
            k += data_window_ok["opt_wind"].__len__() - it - 1
            k_tot += data_window_ok["opt_wind"].__len__() + 5
            path_eval = path_reopt + "evaluation" + str(j)




    N_dat = data_ok.dtype.__len__()
    ok_means = (np.mean(median_reproj_err_ok), np.mean(abs_p_first_ok), np.mean(abs_a_first_ok), np.mean(rms_abs_p_all_ok), np.mean(rms_pos_abs_p_all_scaled_ok))
    ok_std = (np.std(median_reproj_err_ok), np.std(abs_p_first_ok), np.std(abs_a_first_ok), np.std(rms_abs_p_all_ok), np.std(rms_pos_abs_p_all_scaled_ok))
    # ok_means = (np.mean(median_reproj_err_ok), np.mean(abs_p_first_ok), np.mean(abs_a_first_ok), np.mean(abs_p_last), np.mean(abs_a_last), np.mean(rms_abs_p_all_ok), np.mean(rms_pos_abs_p_all_scaled_ok))
    # ok_std = (np.std(median_reproj_err_ok), np.std(abs_p_first_ok), np.std(abs_a_first_ok), np.std(abs_p_last), np.std(abs_a_last), np.std(rms_abs_p_all_ok), np.std(rms_pos_abs_p_all_scaled_ok))

    ind = np.arange(N_dat) + 0.15 # the x locations for the groups
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

    autolabel(rects1)
    autolabel(rects2)

#relative bars
    N_dat2 = data_ok.dtype.__len__()

    if (not median_reproj_err.__len__() == 0) and np.isnan(median_reproj_err[-1]):
        means = (np.nan, np.nan, np.nan, np.mean(rms_abs_p_all),
                 np.mean(rms_pos_abs_p_all_scaled))
        std = (np.nan, np.nan, np.nan, np.std(rms_abs_p_all), np.std(rms_pos_abs_p_all_scaled))
    else:
        means = (np.mean(median_reproj_err), np.mean(abs_p_first), np.mean(abs_a_first), np.mean(rms_abs_p_all),
                 np.mean(rms_pos_abs_p_all_scaled))
        std = (np.std(median_reproj_err), np.std(abs_p_first), np.std(abs_a_first), np.std(rms_abs_p_all), np.std(rms_pos_abs_p_all_scaled))

    ind = np.arange(N_dat) + 0.2 # the x locations for the groups
    width = 0.6       # the width of the bars

    fig, ax = plt.subplots()
    rects3 = ax.bar(ind, means, width, color='r', yerr=std, error_kw=dict(ecolor='black'))
    autolabel(rects3)

    # add some text for labels, title and axes ticks
    ax.set_ylabel('%')
    ax.set_title('results of reoptimization relative to OKVIS (window-wise)')
    ax.set_xticks(ind + width/2)
    ax.set_xticklabels(('median_reproj_err', 'abs_p_first', 'abs_a_first', 'rms_abs_p_all', 'rms_pos_abs_p_all_scaled'))

    ax.legend('reopt')
    plt.axhline(y=100, xmin=0, xmax=10, linewidth=2, color = 'green')
    ylims = ax.get_ylim()
    #ax.set_ylim((0, ylims[1]))
    ax.set_ylim(0, 700)

    sizes, labels, total_t = plot_time.import_time_data(rec_paths)
    sizes[:] = [s / c for s in sizes]
    total_t = total_t / c


#time
    fig1, ax1 = plt.subplots()
    plt.suptitle("total time: %0.1f" % total_t + "s")
    ax1.set_xlabel("%0.1f" % (float(k)/c) + " reoptimized keyframes per window" + "\n %0.1f" % (float(k_tot)/c) + " keyframes per window")

    cmap = plt.cm.jet
    colors = cmap([0.1, 0.4, 0.7, 1, 0.4, 0.7, 1])
    ax1.pie(sizes, labels=labels, pctdistance=0.75, autopct=plot_time.make_autopct(sizes),
            shadow=False, startangle=90, colors=colors)  # explode=explode, autopct='%1.1f%%', autopct='%.1f'
    ax1.axis('equal')

# matches
    length = len(sorted(matches_cnt,key=len, reverse=True)[0])
    matches_cnt_mat=np.array([[0]*(length-len(xi)) + xi for xi in matches_cnt])


    fig2, ax2 = plt.subplots()
    mean_matches_cnt = np.mean(matches_cnt_mat, 0)
    x_ax = np.arange(-mean_matches_cnt.__len__(), 0, 1)

    #print x_ax
    #print mean_matches_cnt

    ax2.plot(x_ax, matches_cnt_mat.T * 100)
    ax2.plot(x_ax, mean_matches_cnt * 100, color="red", lw=4.0)
    ax2.set_xlabel("kf in overlap")
    ax2.set_ylabel("% of matches")

# scale scatters
    fig3, axes = plt.subplots(nrows=1, ncols=3)
    fig3.patch.set_facecolor('white')
    ax1, ax2, ax3 = axes.flatten()

    ax1.scatter(scale_overlap, scale_flex_ok, label='reopt window')
    ax1.set_xlabel("scale overlap (fixed)", fontsize=20)
    ax1.set_ylabel("scale reoptimization window", fontsize=20)
    ax1.set_title("OKVIS", fontsize=20)
    x0,x1 = ax1.get_xlim()
    y0,y1 = ax1.get_ylim()
    low = min(x0, y0)
    up = max(x1, y1)
    m,b = np.polyfit(scale_overlap, scale_flex_ok, 1)
    #ax1.plot([low, up],[low * m + b, up * m + b])
    ax1.legend(loc=0, fontsize=16)

    # model_ransac = linear_model.RANSACRegressor(linear_model.LinearRegression(), min_samples=int(0.8*scale_overlap.__len__()))
    # model_ransac.fit(np.array(scale_overlap).reshape(-1, 1), np.array(scale_flex_ok).reshape(-1, 1))
    # # Predict data of estimated models
    # line_X = np.arange(-5, 5)
    # line_y_ransac = model_ransac.predict(line_X[:, np.newaxis])
    # ax1.plot(line_X, line_y_ransac, color='cornflowerblue', linestyle='-',
    #          linewidth=1, label='RANSAC regressor')

    ax1.set_xlim((low, up))
    ax1.set_ylim((low, up))
    ax1.set_aspect(1)


    ax2.scatter(scale_overlap, scale_flex_re, label='reopt window')
    ax2.set_xlabel("scale overlap (fixed)", fontsize=20)
    ax2.set_ylabel("scale reoptimization window", fontsize=20)
    ax2.set_title("ours", fontsize=20)
    x0,x1 = ax2.get_xlim()
    y0,y1 = ax2.get_ylim()
    low = min(x0, y0)
    up = max(x1, y1)
    m,b = np.polyfit(scale_overlap, scale_flex_re, 1)
    ax2.plot([low, up],[low * m + b, up * m + b])
    ax2.legend(loc=0, fontsize=16)

    # model_ransac = linear_model.RANSACRegressor(linear_model.LinearRegression(), min_samples=int(0.8*scale_overlap.__len__()))
    # model_ransac.fit(np.array(scale_overlap).reshape(-1, 1), np.array(scale_flex_re).reshape(-1, 1))
    # # Predict data of estimated models
    # line_X = np.arange(-5, 5)
    # line_y_ransac = model_ransac.predict(line_X[:, np.newaxis])
    # ax2.plot(line_X, line_y_ransac, color='cornflowerblue', linestyle='-',
    #          linewidth=1, label='RANSAC regressor')

    ax2.set_xlim((low, up))
    ax2.set_ylim((low, up))
    ax2.set_aspect(1)

    ax3.scatter(scale_overlap, abs_p_first_re)
    ax3.set_xlabel("scale overlap")
    ax3.set_ylabel("position error of final kf")
    ax3.set_title("reopt", fontsize=20)
    x0,x1 = ax3.get_xlim()
    y0,y1 = ax3.get_ylim()
    low = x0
    up = x1
    m,b = np.polyfit(scale_overlap, abs_p_first_re, 1)
    ax3.plot([low, up],[low * m + b, up * m + b])

    # model_ransac = linear_model.RANSACRegressor(linear_model.LinearRegression(), min_samples=int(0.1*scale_overlap.__len__()))
    # model_ransac.fit(np.array(scale_overlap).reshape(-1, 1), np.array(abs_p_first_re).reshape(-1, 1))
    # # Predict data of estimated models
    # line_X = np.arange(-5, 5)
    # line_y_ransac = model_ransac.predict(line_X[:, np.newaxis])
    # ax3.plot(line_X, line_y_ransac, color='cornflowerblue', linestyle='-',
    #          linewidth=1, label='RANSAC regressor')

    # ax3.set_xlim((low, up))
    # ax3.set_ylim((low, up))
    ax3.set_aspect(abs(x1-x0)/abs(y1-y0))

    multipage(os.path.dirname(path) + "/" + str(R) + ".pdf")
    plt.show()
    plt.close('all')

