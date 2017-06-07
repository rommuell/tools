# -*- coding: utf-8 -*-
#
import numpy as np
from glob import glob
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import math
import plot_time
from sklearn import linear_model, datasets


def autolabel(rects, n, add_value=[]):
    """
    Attach a text label above each bar displaying its height
    """
    if rects.__len__() == add_value.__len__():
        for rect, val in zip(rects, add_value):
            height = rect.get_height()
            if not np.isnan(height) or height == 0:
                ax.text(rect.get_x() + rect.get_width()/2., 1.03 * height,
                        ('%1.' + str(n) + 'f') % height + '\n(' + val + ')',
                        ha='center', va='bottom')
    else:
        for rect in rects:
            height = rect.get_height()
            if not (np.isnan(height) or height == 0):
                ax.text(rect.get_x() + rect.get_width()/2., 1.07* height,
                        ('%1.' + str(n) + 'f') % height,
                        ha='center', va='bottom')


#filtering
ind = np.arange(3) + 0.125  # the x locations for the groups
width = 0.25  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind -width, [1.8, 1.8, 1.9], width, color='b', error_kw=dict(ecolor='black'))
rects2 = ax.bar(ind, [1.3, 1.8, 1.0], width, color='orange', error_kw=dict(ecolor='black'))
rects3 = ax.bar(ind + width, [1.2, 1.4, 1.0], width, color='red', error_kw=dict(ecolor='black'))

# add some text for labels, title and axes ticks
ax.set_ylabel('[px]')
ax.set_title('Reprojection error depending on different filtering procedures', fontsize=14.5)
ax.set_xticks(ind + width/2)
ax.set_xticklabels(('Laborit \n away', 'Laborit \n close', 'Quarry'), fontsize=16)
ax.set_ylim((0, 3))

ax.legend((rects1[0], rects2[0], rects3[0]), ('OKVIS', 'geometric filtering', 'ours'))

autolabel(rects1,1)
autolabel(rects2,1)
autolabel(rects3,1)




#without additional features
ind = np.arange(4) + 0.3  # the x locations for the groups
width = 0.4  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, [125, 222, 152, 102], width, color='b', error_kw=dict(ecolor='black'), label='position T-R-aligned')

# add some text for labels, title and axes ticks
ax.set_ylabel('[%]')
ax.set_title('Reoptimization of OKVIS data in bigger window', fontsize=16)
ax.set_xticks(ind + width/2)
ax.set_xticklabels(('Laborit \n away', 'Laborit \n close', 'Quarry', 'HG 13'), fontsize=16)
ax.set_ylim((0, 250))
ax.legend()
ax.axhline(y=100, xmin=0, xmax=10, linewidth=2, color = 'green')

autolabel(rects1,0)



# number of matches
fig2, ax2 = plt.subplots()
x_ax = np.array([-10, -9, -8, -7, -6, -5, -4, -3, -2, -1])
#data from experiments_1, run 29
l2 = np.array([ 0.02572837, 0.02846295, 0.03566811, 0.03491385, 0.05074863, 0.06441951, 0.09266903, 0.14987024, 0.21102079, 0.30649853])
l3 = np.array([ 0.00350386, 0.00505608, 0.01040865, 0.01918539, 0.03092732, 0.06213271, 0.10660194, 0.17327079, 0.24926852, 0.33964475])
q7 = np.array([ 0.04592909, 0.05700096, 0.07259807, 0.08686177, 0.10368366, 0.10623731, 0.11104995, 0.12464281, 0.14095262, 0.15104375])
HG13 = np.array([ 0.01172573, 0.01891052, 0.02907109, 0.03511144, 0.04923691, 0.08231435, 0.11916825, 0.14503651, 0.20082062, 0.30860459])


ax2.plot(x_ax, l2 * 100, lw=2.0, label='Laborit away')
ax2.plot(x_ax, l3 * 100, lw=2.0, label='Laborit close')
ax2.plot(x_ax, q7 * 100, lw=2.0, label='Quarry')
ax2.plot(x_ax, HG13 * 100, lw=2.0, label='HG')

ax2.set_xlabel("kf in overlap")
ax2.set_ylabel("% of matches")
ax2.legend(loc=0)




# results max TTA
ind = np.arange(4) + 0.125  # the x locations for the groups
width = 0.25  # the width of the bars

fig3, ax = plt.subplots()
#data from experiments_1, run 32
rects1 = ax.bar(ind - width, [496, 484, 109, 0], width, color='b', error_kw=dict(ecolor='black'))
rects2 = ax.bar(ind, [110, 122, 124, 93], width, color='orange', error_kw=dict(ecolor='black'))
rects3 = ax.bar(ind  + width, [73, 90, 73, 86], width, color='red', error_kw=dict(ecolor='black'))

# add some text for labels, title and axes ticks
ax.set_ylabel('[%]')
ax.set_title('Our approach vs. OKVIS', fontsize=16)
ax.set_xticks(ind + width/2)
ax.set_xticklabels(('Laborit \n away', 'Laborit \n close', 'Quarry', 'HG'), fontsize=16)
ax.set_ylim((0, 600))

ax.axhline(y=100, xmin=0, xmax=10, linewidth=2, color = 'green')
ax.legend((rects1[0], rects2[0], rects3[0]), ('angle', 'position T-R-aligned', 'position T-R-S-aligned'))

autolabel(rects1,0)
autolabel(rects2,0)
autolabel(rects3,0)
xlim = ax.get_xlim()


# results max TTA without scale aligned
fig4, ax = plt.subplots()
rects1 = ax.bar(ind - width, [496, 484, 109, 0], width, color='b', error_kw=dict(ecolor='black'))
rects2 = ax.bar(ind, [110, 122, 124, 93], width, color='orange', error_kw=dict(ecolor='black'))

# add some text for labels, title and axes ticks
ax.set_ylabel('[%]')
ax.set_title('Our approach vs. OKVIS', fontsize=16)
ax.set_xticks(ind + width/2)
ax.set_xticklabels(('Laborit \n away', 'Laborit \n close', 'Quarry', 'HG'), fontsize=16)
ax.set_ylim((0, 600))
ax.axhline(y=100, xmin=0, xmax=10, linewidth=2, color = 'green')
ax.legend((rects1[0], rects2[0]), ('angle', 'position T-R-aligned'))
ax.set_xlim(xlim)

autolabel(rects1,0)
autolabel(rects2,0)




# results max TTA
ind = np.arange(4) + 0.125  # the x locations for the groups
width = 0.25  # the width of the bars

fig5, ax = plt.subplots()
#data from experiments_1, run 33
rects1 = ax.bar(ind - width, [100, 100, 100, 0], width, color='b', error_kw=dict(ecolor='black'))
rects2 = ax.bar(ind, [109, 125, 116, 98], width, color='orange', error_kw=dict(ecolor='black'))
rects3 = ax.bar(ind  + width, [69, 89, 107, 75], width, color='red', error_kw=dict(ecolor='black'))

# add some text for labels, title and axes ticks
ax.set_ylabel('[%]')
ax.set_title('Our approach vs. OKVIS - rotation locked', fontsize=16)
ax.set_xticks(ind + width/2)
ax.set_xticklabels(('Laborit \n away', 'Laborit \n close', 'Quarry', 'HG'), fontsize=16)
ax.set_ylim((0, 600))

ax.axhline(y=100, xmin=0, xmax=10, linewidth=2, color = 'green')
ax.legend((rects1[0], rects2[0], rects3[0]), ('angle', 'position T-R-aligned', 'position T-R-S-aligned'))

autolabel(rects1,0)
autolabel(rects2,0)
autolabel(rects3,0)
xlim = ax.get_xlim()


# results max TTA without scale aligned
fig6, ax = plt.subplots()
rects1 = ax.bar(ind - width, [100, 100, 100, 0], width, color='b', error_kw=dict(ecolor='black'))
rects2 = ax.bar(ind, [109, 125, 116, 98], width, color='orange', error_kw=dict(ecolor='black'))

# add some text for labels, title and axes ticks
ax.set_ylabel('[%]')
ax.set_title('Our approach vs. OKVIS - rotation locked', fontsize=16)
ax.set_xticks(ind + width/2)
ax.set_xticklabels(('Laborit \n away', 'Laborit \n close', 'Quarry', 'HG'), fontsize=16)
ax.set_ylim((0, 600))
ax.axhline(y=100, xmin=0, xmax=10, linewidth=2, color = 'green')
ax.legend((rects1[0], rects2[0]), ('angle', 'position T-R-aligned'))
ax.set_xlim(xlim)

autolabel(rects1,0)
autolabel(rects2,0)


plt.show()