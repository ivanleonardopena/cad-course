

import matplotlib.pyplot as plt
import numpy as np
from control.matlab import *
from scipy.integrate import odeint


F = 10 #Frecuencia 10hz
Ts = 1/F

h = tf(10,[1, 3, 10])
print(h)
#numt, dent = pade(0.25,1)
#theta = tf(numt, dent)
#h1 = series(h, theta)
hd = c2d(h,Ts, 'zoh')
hd1 = c2d(h,Ts, 'foh')
hd2 = c2d(h,Ts, 'bilinear')

print(hd)

y,t = step(h)
yd,td = step(hd)
yd1,td1 = step(hd1)
yd2,td2 = step(hd2)


plt.plot(t,y, label='Continuo')
plt.step(td,yd, label='ZOH')
plt.step(td1,yd1, label='FOH')
plt.step(td2,yd2, label='Tustin')
plt.legend(loc='best')
plt.show()

#  Implementación del modelo en sistemas embebidos

nit = int(10/0.1)
y = np.zeros(nit)
u = np.zeros(nit)
u[10:] =1
t = np.arange(0,(nit)*0.1,0.1)

B = hd.num[0][0]
A = hd.den[0][0]
d = 0

for k in range(2, nit):
    y[k] = -A[1]*y[k-1]-A[2]*y[k-2]+B[0]*u[k-1-d]+B[1]*u[k-2-d]
    
yout, ts, xout = lsim(hd, u, t)
plt.figure()
plt.plot(ts,yout, t, y, '--')
plt.show()