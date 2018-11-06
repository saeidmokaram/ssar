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

from ssarLib import makeKaldiFormat, makeKaldiFormatAugmented

makeKaldiFormatAugmented("/home/saeid/asr/datasets/ssar", "/home/saeid/asr/datasets/ssar/kaldiData", "/home/saeid/asr/datasets/ssar/noise.wav", [0.0, 0.1, 0.2, 0.3, 0.4, 0.5])