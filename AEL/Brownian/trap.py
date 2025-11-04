import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
downloads_dir = os.path.expanduser('~/Downloads') 


#-------------------- Global variables/Constants ---------------------#
k_B = #Boltzmann's constant
T =  #temperature of the room
d = 3E-6 #diameter of the silica beads
nu = #viscosity of the medium (H_20)



pos_data = np.loadtxt('Brownian_Data/data2.dat', skiprows=2) #position data

var = np.var(pos_data[:, 2]) #variance of the position data
alpha = k_B * T / var #trap strength
beta = 3 * np.pi * nu * d 
f_0 = alpha / (2 * np.pi * beta) #fundamental frequency 
P_0 = 2 * var / (np.pi * f_0) #fundamental power


f = np.linspace(10**(-1), 10**4, 10)
P_x = P_0 * f_0**2 / (f**2 + f_0**2)


plt.figure()
plt.title('Power Spectrum of Different Trap Strengths')
plt.xlabel(f'Frequency {f}')
plt.xscale('log')
plt.ylabel(f'Power {P(f)}')
plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
plt.grid(True, which='both', ls='--', alpha=0.6)
plt.tight_layout()
plt.savefig('Power_Spectrum.png', dpi=300)

plt.plot(f, P_x)
plt.savefig('Power_Spectrum.png')