#!/usr/bin/python
#! -*- encoding: utf-8 -*-

# modified Roman Mueller, 02/2017
import subprocess
import shutil

directory_0s = []
egms = []
configs = []
gts = []

i_0 = 0
N = 25



# directory_0s.append("/media/rm/9480CE0280CDEB36/experiments_1/HG_13/l_")
#
# egms_per_ok = []
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/HG_13/egm_0.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/HG_13/egm_1.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/HG_13/egm_2.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/HG_13/egm_3.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/HG_13/egm_4.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/HG_13/egm_5.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/HG_13/egm_6.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/HG_13/egm_7.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/HG_13/egm_8.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/HG_13/egm_9.yaml")
# egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/HG_13/egm_10.yaml")
# egms.append(egms_per_ok)
#
# configs.append("/config_visensor_mono.yaml")
# gts.append("/leica_data_reordered.csv")
#
#
#
#
# directory_0s.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit_away2/l_")
#
# egms_per_ok = []
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit_away2/egm_0.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit_away2/egm_1.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit_away2/egm_2.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit_away2/egm_3.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit_away2/egm_4.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit_away2/egm_5.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit_away2/egm_6.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit_away2/egm_7.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit_away2/egm_8.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit_away2/egm_9.yaml")
# egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit_away2/egm_10.yaml")
# egms.append(egms_per_ok)
#
# configs.append("/config_blender.yaml")
# gts.append("/poses_reordered.csv")
#
#
#
#
# directory_0s.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit3/l_")
#
# egms_per_ok = []
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit3/egm_0.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit3/egm_1.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit3/egm_2.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit3/egm_3.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit3/egm_4.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit3/egm_5.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit3/egm_6.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit3/egm_7.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit3/egm_8.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit3/egm_9.yaml")
# egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/laborit3/egm_10.yaml")
# egms.append(egms_per_ok)
#
# configs.append("/config_blender.yaml")
# gts.append("/poses_reordered.csv")
#
#
#
#
#
# directory_0s.append("/media/rm/9480CE0280CDEB36/experiments_1/quarry7/l_")
#
# egms_per_ok = []
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/quarry7/egm_0.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/quarry7/egm_1.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/quarry7/egm_2.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/quarry7/egm_3.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/quarry7/egm_4.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/quarry7/egm_5.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/quarry7/egm_6.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/quarry7/egm_7.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/quarry7/egm_8.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/quarry7/egm_9.yaml")
# egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/quarry7/egm_10.yaml")
# egms.append(egms_per_ok)
#
# configs.append("/config_blender.yaml")
# gts.append("/poses_reordered.csv")
#
#
#
#
#
# directory_0s.append("/media/rm/9480CE0280CDEB36/experiments_1/31_ST/l_")
#
# egms_per_ok = []
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/31_ST/egm_0.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/31_ST/egm_1.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/31_ST/egm_2.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/31_ST/egm_3.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/31_ST/egm_4.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/31_ST/egm_5.yaml")
# #egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_1/31_ST/egm_6.yaml")
# egms.append(egms_per_ok)
#
# configs.append("/config_visensor_mono.yaml")
# gts.append("/leica_data_reordered.csv")


directory_0s.append("/media/rm/9480CE0280CDEB36/experiments_2/23_CAB/l_")

egms_per_ok = []
egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_2/23_CAB/egm_10.yaml")
egms.append(egms_per_ok)

configs.append("/config_visensor_mono.yaml")
gts.append("/leica_data_reordered.csv")



directory_0s.append("/media/rm/9480CE0280CDEB36/experiments_2/24_CAB/l_")

egms_per_ok = []
egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_2/24_CAB/egm_10.yaml")
egms.append(egms_per_ok)

configs.append("/config_visensor_mono.yaml")
gts.append("/leica_data_reordered.csv")



directory_0s.append("/media/rm/9480CE0280CDEB36/experiments_2/31_ST/l_")

egms_per_ok = []
egms_per_ok.append("/media/rm/9480CE0280CDEB36/experiments_2/31_ST/egm_10.yaml")
egms.append(egms_per_ok)

configs.append("/config_visensor_mono.yaml")
gts.append("/leica_data_reordered.csv")

for e in range(0, directory_0s.__len__()):
    egms_per_ok = egms[e]
    config = configs[e]
    gt = gts[e]
    directory_0 = directory_0s[e]

    for egm in egms_per_ok:
        for i in xrange(i_0, i_0 + N, 1):
            path = directory_0 + str(i)
            shutil.copy(egm, path + "/egm.yaml")
            command = ["/home/rm/code/egm/build/main",
                        "-i", path + "/okvis_output",
                        "-c", path + config,
                        "-g", path + gt]
            print command
            p = subprocess.Popen(command)
            p.wait()

