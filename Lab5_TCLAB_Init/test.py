# -*- coding: utf-8 -*-
"""
Verificar el funcionamiento del TCLab

@author: Sergio
"""

import tclab_cae.tclab_cae as tclab
import time

#Instanciamos el objeto LAB
lab = tclab.TCLab_CAE() 

print('Turn ON the heaters for 30 seconds')
lab.Q1(50) #Percentage 0 - 100
lab.LED(100)

for i in range(31):
    print('t:', i, 'T1:', lab.T1, 'I1:', lab.I1, 'Ta:', lab.T3)
    time.sleep(1)

lab.Q1(0)
lab.LED(0)
lab.close()
