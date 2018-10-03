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
# Usage:
# data = Recording("/home/saeid/asr/datasets/ssar/map1/start-room1/s001-s002")
# data.writeJson("/home/saeid/asr/datasets/ssar/map1/start-room1/s001-s002/data.json")
# data.plot(True)
# ==============================================

import os, json, math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# ========================================================================
class Recording():
    def __init__(self, dataFolderPath):
        self._makePath(dataFolderPath)
        [self.mainSpeakerID, self.mainSpeakerGender, self.utterances_mainSpeaker, self.audioLen] = self.readTrans(self.transPath_mainSpeaker)
        [self.secondSpeakerID, self.secondSpeakerGender, self.utterances_secondSpeaker, _] = self.readTrans(self.transPath_secondSpeaker)
        [_, _, self.utterances_autoMainSpeaker, _] =  self.readTrans(self.autoTransPath_mainSpeaker)
        [_, _, self.utterances_autoSecondSpeaker, _] = self.readTrans(self.autoTransPath_secondSpeaker)

        self.pos = self.readPOS(self.posPath)

    # ========================================================================
    def _makePath(self, dataFolderPath):
        self.dataFolderPath = dataFolderPath
        self.posPath = self.dataFolderPath + "/pos.txt"
        self.transPath_mainSpeaker = dataFolderPath + "/transcript/m-ch.trs"
        self.transPath_secondSpeaker = dataFolderPath + "/transcript/s-ch.trs"
        self.autoTransPath_mainSpeaker = dataFolderPath + "/auto-transcript/m-ch.trs"
        self.autoTransPath_secondSpeaker = dataFolderPath + "/auto-transcript/s-ch.trs"
        self.audioPath_mainSpeaker = dataFolderPath + "/16kHz_16bit/m-ch.wav"
        self.audioPath_secondSpeaker = dataFolderPath + "/16kHz_16bit/s-ch.wav"
        self.audioPath_noise = dataFolderPath + "/16kHz_16bit/noise.wav"

    # ========================================================================
    def readTrans(self, transPath):
        utterances = []
        speakerID = None
        gender = None
        audioLen = None

        if os.path.exists(transPath):
            text = ""

            with open(transPath, "r") as transFile:
                lines = transFile.readlines()

            for i, line in enumerate(lines):
                if line.startswith("<Turn startTime="):
                    splt = line.split()
                    audioLen = float(splt[2].split('"')[1])
                elif line.startswith("<Speaker id="):
                    splt = line.split()
                    speakerID = str(splt[2].split('"')[1])
                    gender = str(splt[4].split('"')[1])
                elif line.startswith('<Sync time='):
                    time = float(line.split('"')[1])
                    if len(text):
                        endT = time
                        utterances.append( {"start_time": stratT, "end_time":endT, "duration":endT-stratT, "text": text} )
                        text = ""
                    elif time:
                        stratT = time
                        text = lines[i+1].strip()

        return [speakerID, gender, utterances, audioLen]

    # ========================================================================
    def readPOS(self, POSPath):
        with open(POSPath, "r") as transFile:
            lines = transFile.readlines()

        pos = []
        for line in lines:
            if line.startswith("tim("):
                splt = line.split()
                time = float(splt[0][4:-1])
                x = float(splt[1][4:-1])
                z = float(splt[2][:-1])
                y = float(splt[3][:-1])
                r = float(splt[4][4:-1])
                p = float(splt[5][:-1])
                q = float(splt[6][:-1])

                pos.append( {"time":time, "x":x, "y":y, "z":z, "roll":r, "pitch":p, "yaw":q} )
        return pos

    # ========================================================================
    def writeJson(self, outPath):
        dataDict = {"utterances_ch1": self.utterances_mainSpeaker,
                    "utterances_ch2": self.utterances_secondSpeaker,
                    "gender_ch1": self.mainSpeakerGender,
                    "gender_ch2": self.secondSpeakerGender,
                    "duration": self.audioLen,
                    "speakerID_ch1": self.mainSpeakerID,
                    "speakerID_ch2": self.secondSpeakerID,
                    "pos": self.pos
                    }

        with open(outPath, 'w') as outfile:  # Saving data.
            json.dump(dataDict, outfile, indent=4)

    # ========================================================================
    def plot(self, show_scene):

        x = [p["x"] for p in self.pos]
        y = [p["y"] for p in self.pos]
        o = [p["pitch"] for p in self.pos]

        plt.plot(x, y, 'b-')
        plt.plot(x[0], y[0], 'ro')

        for i in range(len(x)):
            plt.arrow(x[i], y[i], math.sin(math.radians(o[i])), math.cos(math.radians(o[i])), head_width=0.05, head_length=0.1, fc='g', ec='g')



        if (10 <= x[0] <= 40) and (-40 <= y[0] <= -10):  # ------ Map 1 ------
            if not show_scene:
                plt.plot([10,10],[-40,-10],'gray',linewidth = 10)
                plt.plot([40,40],[-40,-10],'gray',linewidth = 10)
                plt.plot([10,40],[-10,-10],'gray',linewidth = 10)
                plt.plot([10,40],[-40,-40],'gray',linewidth = 10)

                plt.plot([10,16],[-20,-20],'gray',linewidth = 10)
                plt.plot([19,36],[-20,-20],'gray',linewidth = 10)
                plt.plot([39,40],[-20,-20],'gray',linewidth = 10)

                plt.plot([10,11],[-30,-30],'gray',linewidth = 10)
                plt.plot([14,31],[-30,-30],'gray',linewidth = 10)
                plt.plot([34,40],[-30,-30],'gray',linewidth = 10)

                plt.plot([20,20],[-40,-34],'gray',linewidth = 10)
                plt.plot([20,20],[-31,-14],'gray',linewidth = 10)
                plt.plot([20,20],[-11,-10],'gray',linewidth = 10)

                plt.plot([30,30],[-40,-39],'gray',linewidth = 10)
                plt.plot([30,30],[-36,-19],'gray',linewidth = 10)
                plt.plot([30,30],[-16,-10],'gray',linewidth = 10)
            else:
                img=mpimg.imread('map1.png')
                plt.imshow(img, origin='lower', extent=[10,40,-10,-40])

            plt.xlim(8,42)
            plt.ylim(-42,-8)

        elif (-40 <= x[0] <= -10) and (0 <= y[0] <= 40):  # ------ Map 2 ------
            if not show_scene:
                plt.plot([-10,-10],[10,30],'gray',linewidth = 10)
                plt.plot([-40,-40],[10,30],'gray',linewidth = 10)
                plt.plot([-20,-30],[0,0],'gray',linewidth = 10)
                plt.plot([-20,-30],[40,40],'gray',linewidth = 10)

                plt.plot([-40,-29],[10,10],'gray',linewidth = 10)
                plt.plot([-26,-10],[10,10],'gray',linewidth = 10)


                plt.plot([-40,-29],[30,30],'gray',linewidth = 10)
                plt.plot([-26,-10],[30,30],'gray',linewidth = 10)

                plt.plot([-40,-24],[20,20],'gray',linewidth = 10)
                plt.plot([-21,-10],[20,20],'gray',linewidth = 10)

                plt.plot([-20,-20],[0,11],'gray',linewidth = 10)
                plt.plot([-20,-20],[14,26],'gray',linewidth = 10)
                plt.plot([-20,-20],[29,40],'gray',linewidth = 10)

                plt.plot([-30,-30],[0,16],'gray',linewidth = 10)
                plt.plot([-30,-30],[19,21],'gray',linewidth = 10)
                plt.plot([-30,-30],[24,40],'gray',linewidth = 10)
            else:
                img=mpimg.imread('map2.png')
                plt.imshow(img, origin='lower', extent=[-40,-10,40,0])

            plt.xlim(-42,-8)
            plt.ylim(-2,42)

        elif (-40 <= x[0] <= -10) and (-40 <= y[0] <= 0):  # ------ Map 3 ------
            if not show_scene:
                plt.plot([-10,-10],[-20,-0],'gray',linewidth = 10)
                plt.plot([-40,-40],[-40,-20],'gray',linewidth = 10)
                plt.plot([-30,-10],[0,0],'gray',linewidth = 10)
                plt.plot([-40,-20],[-40,-40],'gray',linewidth = 10)

                plt.plot([-30,-29],[-10,-10],'gray',linewidth = 10)
                plt.plot([-26,-14],[-10,-10],'gray',linewidth = 10)
                plt.plot([-11,-10],[-10,-10],'gray',linewidth = 10)

                plt.plot([-40,-24],[-20,-20],'gray',linewidth = 10)
                plt.plot([-21,-10],[-20,-20],'gray',linewidth = 10)
                plt.plot([39,40],[-20,-20],'gray',linewidth = 10)

                plt.plot([-40,-34],[-30,-30],'gray',linewidth = 10)
                plt.plot([-31,-29],[-30,-30],'gray',linewidth = 10)
                plt.plot([-26,-20],[-30,-30],'gray',linewidth = 10)

                plt.plot([-20,-20],[-40,-14],'gray',linewidth = 10)
                plt.plot([-20,-20],[-11,-9],'gray',linewidth = 10)
                plt.plot([-20,-20],[-6,0],'gray',linewidth = 10)

                plt.plot([-30,-30],[-40,-39],'gray',linewidth = 10)
                plt.plot([-30,-30],[-36,-24],'gray',linewidth = 10)
                plt.plot([-30,-30],[-21,-0],'gray',linewidth = 10)
            else:
                img=mpimg.imread('map3.png')
                plt.imshow(img, origin='lower', extent=[-40,-10,0,-40])

            plt.xlim(-42,-8)
            plt.ylim(-42,2)

        elif (10 <= x[0] <= 40) and (0 <= y[0] <= 40):  # ------ Map 4 ------
            if not show_scene:
                plt.plot([10,10],[10,30],'gray',linewidth = 10)
                plt.plot([40,40],[10,40],'gray',linewidth = 10)
                plt.plot([30,40],[40,40],'gray',linewidth = 10)
                plt.plot([20,30],[0,0],'gray',linewidth = 10)

                plt.plot([10,26],[10,10],'gray',linewidth = 10)
                plt.plot([29,40],[10,10],'gray',linewidth = 10)

                plt.plot([10,16],[20,20],'gray',linewidth = 10)
                plt.plot([19,21],[20,20],'gray',linewidth = 10)
                plt.plot([24,36],[20,20],'gray',linewidth = 10)
                plt.plot([39,40],[20,20],'gray',linewidth = 10)

                plt.plot([10,31],[30,30],'gray',linewidth = 10)
                plt.plot([34,40],[30,30],'gray',linewidth = 10)

                plt.plot([20,20],[0,11],'gray',linewidth = 10)
                plt.plot([20,20],[14,26],'gray',linewidth = 10)
                plt.plot([20,20],[29,30],'gray',linewidth = 10)

                plt.plot([30,30],[0,16],'gray',linewidth = 10)
                plt.plot([30,30],[19,21],'gray',linewidth = 10)
                plt.plot([30,30],[24,40],'gray',linewidth = 10)
            else:
                img=mpimg.imread('map4.png')
                plt.imshow(img, origin='lower', extent=[10,40,40,0])

            plt.xlim(8,42)
            plt.ylim(-2,42)

        plt.show()
# ========================================================================