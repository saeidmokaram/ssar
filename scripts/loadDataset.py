#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Saeid Mokaram"
__copyright__ = "Copyright 2018 The University of Sheffield"
__credits__ = ["Saeid Mokaram, The Sheffield University"]
__license__ = "The University of Sheffield, SPandH"
__version__ = "1.0"
__maintainer__ = "Saeid Mokaram"
__email__ = "saeid.mokaram@gmail.com"
__status__ = "Release"
# ==============================================

from ssarLib import Recording
import os

# ==============================================

def loadSSAR(ssarPath):
    dataset = []
    for map in ["map1", "map2", "map3", "map4"]:
        for startRoom in os.listdir(ssarPath + "/" + map):
            for recording in os.listdir(ssarPath + "/" + map + "/" + startRoom):
                dataFolderPath = ssarPath + "/" + map + "/" + startRoom + "/" + recording
                print(dataFolderPath)

                dataset.append(Recording(dataFolderPath))
    return dataset

# ==============================================

dataset = loadSSAR("..")

print(" ".join( [utt["text"] for utt in dataset[0].utterances_mainSpeaker] ))
dataset[0].plot(True)