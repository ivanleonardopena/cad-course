# -*- coding: utf-8 -*-
"""
Solución de EDO

@author: Sergio
"""
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
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
        self.data = None

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
        
    def set_data(self, data_base):
        self.data = data_base
        
    def calcular_posicion_osc(self, par):
        y0 = np.array(self.x0)
        ym = np.ones(len(self.time_eval)) * self.x0[0] #Posicion
        for i in range(len(self.time_eval)-1):
            ts = [self.time_eval[i], self.time_eval[i+1]]
            sol = solve_ivp(self.vanderpol, ts, y0, method=self.metodo, args=(self.u, par[0]))
            y0 = sol.y[:,-1] #[posicion, velocidad]
            ym[i+1] = y0[0]
        return ym 
        
    def fun_obj(self, par):
        x = self.calcular_posicion_osc(par)
        j = np.sum( ((self.data - x)/self.data )**2 )
        return j
        
        
    def optimize(self):
        #Variable de desicion (mu)
        p = [self.mu]
        sol = minimize(self.fun_obj, p, method='SLSQP', bounds=None)
        self.mu = sol.x[0]
        return sol
        
        

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
    
    #Cargar la base de datos
    data = np.loadtxt('data_vanderpol.txt', delimiter=',', skiprows = 1)
    t = data[:,0].T
    xreal = data[:,1].T
    
    #Actualizar los datos de mi instancia
    oscilador.set_data(xreal)
    oscilador.t_span = [t[0], t[-1]]
    oscilador.time_eval = t
    
    #Resolvemos la EDO inicial cuando no hemos optimizado
    oscilador.resolver()
    xinit = np.copy(oscilador.y)
    
    #Costo inicial antes de la optimización
    j_init = oscilador.fun_obj([mu])
    print(f'The initial cost is {j_init}')
    
    #Proceso de Optimización
    solution = oscilador.optimize()
    print(solution)
    print(f'The optimize mu is {oscilador.mu}')
    
    #Costo final despues de la optimización
    j_fin = oscilador.fun_obj([oscilador.mu])
    print(f'The initial cost is {j_fin}')
    
    oscilador.resolver()
    xfin = np.copy(oscilador.y)
    
    
    
    #Grafica comparación (posicion)
    plt.plot(t, xinit[0], 'b:', linewidth=3,label='Initial Guess')
    plt.plot(t, xreal, 'r-', linewidth=3,label='from data')
    plt.plot(t, xfin[0], 'k--', linewidth=3,label='Final prediction')
    plt.legend(loc='best')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('posición')
    plt.show()
