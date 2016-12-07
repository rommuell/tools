#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import numpy as np
import time
import os

# settings
path = '/home/rm/Documents/master_thesis/data/okvis_output'
maxWindow = 18  # for matches listing (number of keyframes)
n_zeros = 8
# end settings

tic = time.time()

if not os.path.exists(path):
    os.mkdir(os.path.dirname(path) + "/okvis_output")

# open onpenMVG feat file (write)
if not os.path.exists(path + '/matches'):
    os.mkdir(path + '/matches')
matchFile = open(path + '/matches/matches.f.txt', 'w+')

matchWriter = csv.writer(matchFile, delimiter=' ', dialect='excel', quoting=csv.QUOTE_NONE)
matchBuffer = []

keyframes = np.genfromtxt(path + '/keyframeList.csv', dtype='int', delimiter=',')
keyframes_sorted = sorted(map(str, keyframes))  # because openMVG image list is in string-sort order

# write .feat files

for k in keyframes:
    # open onpenMVG feat file (write)
    featFile = open('{0}/matches/{1}.feat'.format(path, str(k).zfill(n_zeros)), 'w+')
    featWriter = csv.writer(featFile, delimiter=' ')

    # open ovis keypoint file (read)
    kpFile1 = open('{0}/{1}.kp'.format(path, str(k).zfill(n_zeros)))
    keypoints1 = csv.DictReader(kpFile1)

    for row in keypoints1:
        featWriter.writerow( [ float(row['keypoint_x']), float(row['keypoint_y']), 0.0, 0.0 ] )

    featFile.close()

# write match file
k_c = 0
for k in keyframes:  # iterate over keyframes
    tic2 = time.time()

    # open okvis keypoint file (read)
    kpFile1 = open('{0}/{1}.kp'.format(path, str(k).zfill(n_zeros)))
    keypoints1 = csv.DictReader(kpFile1)

    k2_c = k_c + 1
    for k2 in keyframes[k_c + 1:]:  # iterate over second keyframes
        if k2_c - k_c > maxWindow:  # speedup
            break

        # open okvis second keypoint file (read)
        kpFile2 = open('{0}/{1}.kp'.format(path, str(k2).zfill(n_zeros)))
        keypoints2 = csv.DictReader(kpFile2)

        i = 1  # line counter

        for row in keypoints1:  # iterate over keypoints of keyframe

            j = 1  # line counter
            for row2 in keypoints2:  # iterate over keypoint in second keypoint file
                if row['landmarkId'] == row2['landmarkId']:
                    matchBuffer.append((i, j))
                    break  # because only one match
                j += 1

            kpFile2.seek(1, 0) # goto begin
            next(kpFile2) # ignore header
            i += 1

        kpFile2.close()
        kpFile1.seek(1, 0) #goto begin
        next(kpFile1) # ignore header


        # write buffer to matches file
        if len(matchBuffer) > 0:
            matchWriter.writerow((k_c, k2_c))
            #matchWriter.writerow((keyframes_sorted.index(str(k)), keyframes_sorted.index(str(k2))))
            matchWriter.writerow([len(matchBuffer)])
            for it in matchBuffer:
                matchWriter.writerow((it[0], it[1]))
            matchBuffer = []

        k2_c += 1

    kpFile1.close()
    print(k_c, time.time() - tic2)
    k_c += 1

matchFile.close()
print('total time:', time.time() - tic)
