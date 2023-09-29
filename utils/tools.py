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
    
class SignalGenerator:
    @staticmethod
    def create_prbs(ValUinit, ValAmpli, ValDecal, ValLgReg, ValDivi, Nsamp, Tappli):
        """
        
        CREATE_PRBS  is used for the generation of a PRBS signal

           prbs = create_prbs(ValUinit, ValAmpli, ValDecal, ValLgReg, ValDivi, Nsamp, Tappli)             

       "Entry parameters" are :
    	ValUinit  : Initial steady state
        ValAmpli  : Magnitude
        ValDecal  : Add-on DC component
        ValLgReg  : Register length
        ValDivi   : Frequency divider
        Nsamp     : Number of samples
        Tappli    : Application instant 
    	  
     
     

    	              ____  Valdecal + ValAmpli         __________      ____
                     |    |                            |          |    |
     Valdecal       -|----|--------                    |          |    |
                     |    |____________________________|          |____|
                     |
                     |
     ini ____________|
                                                       |--------->|
         |-Tappli -->|                        ValReg * ValDivi 
         

         |---------- Nsamp ------------------------------------------------->|
                            
        
    	"Exit parameter" is  :
        prbs : prbs sequence created by PRBS algo

        """
        k1 = ValLgReg - 1
        k2 = ValLgReg
        if ValLgReg == 5:
            k1 = 3
        elif ValLgReg == 7: 
            k1 = 4
        elif ValLgReg == 9:   
            k1 = 5
        elif ValLgReg == 10: 
            k1 = 7
        elif ValLgReg == 11: 
            k1 = 9    
        
        sbpa = [1]*11
        prbs = [0] * (Nsamp + Tappli)
        
        for i in range(Tappli):
           prbs[i] = ValUinit;
        
        i = Tappli + 1
        while i <= Nsamp:
            uiu = -sbpa[k1]*sbpa[k2]
            if ValLgReg == 7:
                uiu = -sbpa[1]*sbpa[2]*sbpa[4]*sbpa[7]
            
            j = 0
            while j <= ValDivi:
                prbs[i] = uiu * ValAmpli + ValDecal
                i += 1
                j += 1
            
            for j in range(ValLgReg, 0 , -1):
                sbpa[j] = sbpa[j - 1]
            
            sbpa[0] = uiu;
        
        return prbs