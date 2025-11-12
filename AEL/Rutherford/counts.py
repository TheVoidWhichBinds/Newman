import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
downloads_dir = os.path.expanduser('~/Downloads') 

#------------ Global Variables ------------#
r_i = 2.3 #[cm]
r_o = 2.7 #[cm]
r_1 = (r_i + r_o)/2
X = 7.22 #[cm]



#------------ Downloading Data -------------#
# data = pd.read_excel('Rutherford_Data.xlsx')
# N_2 = data[:,2]/(5*60) #counts/(5min * 60sec/min)
# Y = data[:,1] #*multiplicative factor


#------------- Theoretical Calculations -------------#
def theory():
    Y_t= np.linspace(1,20,100)
    theta_1 = np.arctan(r_1/X)
    theta_2 = np.pi/2 - np.arctan(Y_t/r_1)
    theta = theta_1 + theta_2
    fY_t = np.cos(theta_2) * (np.sin(theta_2))**2 / (np.sin(theta/2))**4
    return Y_t, fY_t




#------------- Plotting -----------------#
#Theoretical Y_t vs f(Y_t):
plt.figure()
plt.xlabel('Foil Detector Distance Y [cm]')
plt.ylabel('Angular Dependence of Count Rate f(Y)')
plt.title('')
Y_t, fY_t = theory()
plt.plot(Y_t, fY_t)
plt.savefig('f(Y).png')

#
