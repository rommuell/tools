#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import csv

# http://stackoverflow.com/questions/4870393/rotating-coordinate-system-via-a-quaternion
def q_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return w, x, y, z

def q_conjugate(q):
    w, x, y, z = q
    return (w, -x, -y, -z)

def qv_mult(q1, v1):
    q2 = (0.0,) + v1
    return q_mult(q_mult(q1, q2), q_conjugate(q1))[1:]

# settings
path = '/home/rm/Documents/master_thesis/data/okvis_output'
n_zeros = 8
# end settings

keyframes = np.genfromtxt(path + '/keyframeList.csv', dtype='int', delimiter=',')

extrList = []
extrList.append('    "extrinsics": [')

# loop over keyframes
k_c = 0
for k in keyframes:
    twcFile = open(path + '/' + str(k).zfill(n_zeros) + '.twc')
    twcReader = csv.DictReader(twcFile)

    for lastrow in twcReader: pass
    row = lastrow # set lag here
    twc = (float(row['p_T_WC_x']), float(row['p_T_WC_y']), float(row['p_T_WC_z']))
    qwc = (float(row['q_T_WC_w']), float(row['q_T_WC_x']), float(row['q_T_WC_y']), float(row['q_T_WC_z']))

    if int(row['keyFrame']) != k:
        print('error: keyframes are not identical')
        break

    extrList.append('        {')
    extrList.append('            "key": ' + str(k_c) + ',')
    extrList.append('            "value": {')
    extrList.append('                "rotation": [')

    extrList.append('                    [')
    x = qv_mult(qwc, (1, 0, 0))
    extrList.append('                        ' + str(x[0]) + ',')
    extrList.append('                        ' + str(x[1]) + ',')
    extrList.append('                        ' + str(x[2]))
    extrList.append('                    ],')

    extrList.append('                    [')
    y = qv_mult(qwc, (0, 1, 0))
    extrList.append('                        ' + str(y[0]) + ',')
    extrList.append('                        ' + str(y[1]) + ',')
    extrList.append('                        ' + str(y[2]))
    extrList.append('                    ],')

    extrList.append('                    [')
    z = qv_mult(qwc, (0, 0, 1))
    extrList.append('                        ' + str(z[0]) + ',')
    extrList.append('                        ' + str(z[1]) + ',')
    extrList.append('                        ' + str(z[2]))
    extrList.append('                    ]')
    extrList.append('                ],')

    extrList.append('                "center": [')
    extrList.append('                    ' + str(twc[0]) + ',')
    extrList.append('                    ' + str(twc[1]) + ',')
    extrList.append('                    ' + str(twc[2]))

    extrList.append('                ]')
    extrList.append('            }')
    extrList.append('        },')

    k_c += 1

# remove last comma
extrList.pop()
extrList.append('        }')


extrList.append('    ],')
twcFile.close()

extrList.append('    "structure": [],')
extrList.append('    "control_points": []')
extrList.append('}')


# open image list
with open(path + '/knownposes/matches/sfm_data.json') as sfmFile:
    sfm_list = sfmFile.read().splitlines()
sfmFile.close()

# merge lists
sfm_list = sfm_list[:len(sfm_list)-4]
sfm_list.extend(extrList)

# open overwrite image list
with open(path + '/knownposes/matches/sfm_data_pose.json', 'w+') as sfmFile:
    sfmFile.writelines('\n'.join(sfm_list))
sfmFile.close()