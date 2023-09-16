import sys
import numpy as np
import matplotlib.pyplot as plt
import time

# Añadir el directorio superior al path para acceder a la subcarpeta utils
#sys.path.append('C:\\Users\\Sergio\\My Drive\\Clases\\Control Digital\\cad-course')
sys.path.append('../')

from utils.tools import DataSaver, SamplingTime
import tclab_cae.tclab_cae as tclab

class TCLabExperiment:

    def __init__(self, time, step_input, data_name ='data.txt', figure_name = 'test_model.png'):
        self.lab = tclab.TCLab_CAE()
        self.run_time = time                         # Run time in minutes
        self.loops = int(60.0 * self.run_time)       # Transform into the Number of cycles
        
        self.T1 = np.ones(self.loops) * self.lab.T1  # Temperature (C)
        self.Q1 = np.zeros(self.loops)               # impulse tests (0 - 100%)
        self.tm = np.zeros(self.loops)
        self.step_input = step_input
        self.data_name = data_name
        self.figure_name = figure_name

    def run(self):
        self._initialize_experiment()

        try:
            self._main_loop()
            self._finalize_experiment()

        except KeyboardInterrupt:
            self._shutdown("Shutting down")
            
        except RuntimeError:
            self._shutdown("Failed to Connect.")

        except:
            self._shutdown("Error: Shutting down")
            raise

    def _initialize_experiment(self):
        print('LED On')
        self.lab.LED(100)
        self.Q1[10:] = self.step_input  # step input
        plt.figure(figsize=(10,7))
        plt.ion()
        plt.show()

    def _main_loop(self):
        start_time = time.time()
        prev_time = start_time

        for k in range(1, self.loops):
            sleep_max = 1.0
            sleep = sleep_max - (time.time() - prev_time)
            if sleep >= 0.01:
                time.sleep(sleep-0.01)
            else:
                time.sleep(0.01)

            t = time.time()
            dt = t - prev_time
            prev_time = t
            self.tm[k] = t - start_time
            self.T1[k] = self.lab.T1
            self.lab.Q1(self.Q1[k])

            self._update_plot(k)

    def _update_plot(self, k):
        plt.clf()
        ax = plt.subplot(2, 1, 1)
        ax.grid()
        plt.plot(self.tm[:k], self.T1[:k], 'r-', label=r'$T_1$ measured', linewidth=2)
        plt.ylabel('Temperature (C)')
        plt.legend(loc='best')

        ax = plt.subplot(2, 1, 2)
        ax.grid()
        plt.plot(self.tm[:k], self.Q1[:k], 'r-', label=r'$Q_1$', linewidth=2)
        plt.ylabel('Heater')
        plt.xlabel('Time (sec)')
        plt.legend(loc='best')
        plt.draw()
        plt.pause(0.05)

    def _finalize_experiment(self):
        self._shutdown("Experiment completed")

    def _shutdown(self, message):
        print(message)
        self.lab.Q1(0)
        self.lab.Q2(0)
        self.lab.LED(0)
        self.lab.close()
        DataSaver.save_txt(self.tm, self.Q1, self.T1, self.data_name)
        plt.savefig(self.figure_name)

if __name__ == "__main__":
    time_duration = 15.0
    step = 50
    experiment = TCLabExperiment(time_duration, step)
    experiment.run()
