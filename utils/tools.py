# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 00:11:27 2023

@author: Sergio
"""

import matplotlib.pyplot as plt
from control.matlab import *
import numpy as np
from math import pi


class DataSaver:
    @staticmethod
    def save_txt(t, u1, y1, filename='data.txt'):
        data = np.vstack((t,u1,y1)).T
        top = 'Time (sec), Heater 1 (%), Temperature 1 (degC)'
        np.savetxt(filename, data, delimiter=',', header=top, comments='')


class SamplingTime:
    
    @staticmethod
    def calculate(sys):
        h = feedback(sys)
        mag, phase, w = bode(sys)
        m0 = mag[0]
        mWc = 0.707 * m0
        index_wc = np.where(mag >=  mWc)
        wc = w[index_wc[0][-1]]
        wmin = 8 * wc
        wmax = 12*wc
        ts_small = 2*pi / (wmax)
        ts_big = 2*pi / (wmin)
        return (ts_small + ts_big)/2