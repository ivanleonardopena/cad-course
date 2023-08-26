# -*- coding: utf-8 -*-
"""
Solución de EDO

@author: Sergio
"""
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import numpy as np

class OsciladorVanDerPol:
    def __init__(self, x0, u, mu, t_span, metodo = 'Radau', time_eval = None):
        self.x0 = x0
        self.u = u
        self.mu = mu
        self.t_span = t_span
        self.metodo = metodo
        self.time_eval = time_eval 

    def vanderpol(self, t, x, u, mu):
        #Renombrar las salidas
        x1 = x[0]
        x2 = x[1]
        #Renombrar las entrada
        # Q = u

        #EDO
        dx1dt = x2
        dx2dt = mu*(1-x1**2)*x2-x1
        #salida
        dxdt = [dx1dt, dx2dt]
        return dxdt

    def resolver(self):
        sol = solve_ivp(self.vanderpol, self.t_span, self.x0, method=self.metodo, args=(self.u, self.mu), t_eval=self.time_eval)
        self.y = sol.y
        self.t = sol.t

    def graficar(self):
        plt.plot(self.t, self.y[:][0])
        plt.xlabel('Tiempo (s)')
        plt.ylabel('posición')
        plt.show()

if __name__ == '__main__':
    rigido = False
    x0 = [2, 0]
    u = 0
    if rigido:
        t_span = [0, 3000]
        mu = 1000
        metodo = 'Radau'
        time_eval = None
    else:
        t_span = [0, 30]
        pts = int(t_span[-1]/0.1)
        time_eval = np.linspace(0, 30, pts)
        mu = 1
        metodo = 'RK45'

    oscilador = OsciladorVanDerPol(x0, u, mu, t_span, metodo, time_eval)
    oscilador.resolver()
    oscilador.graficar()
