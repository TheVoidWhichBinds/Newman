import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
downloads_dir = os.path.expanduser('~/Downloads') 


#-------- Global variables/Constants --------#
k_B = 1.380649E-23 #Boltzmann's constant [J/K]
T = 298 #temperature of the room [K]
d = 3E-6 #diameter of the silica beads [m]
nu = 8.9E-4 #viscosity of the medium (H_20) [Pa*s]


#---------------------------- Data Downloads -----------------------------#
position = np.loadtxt('Brownian_Data/data2.dat', skiprows=2) #position data

#force data for different laser intensities
force_150mA = np.loadtxt('Brownian_Data/force150.FDdat')
force_200mA = np.loadtxt('Brownian_Data/force200.FDdat')
force_250mA = np.loadtxt('Brownian_Data/force250.FDdat')
force_300mA = np.loadtxt('Brownian_Data/force300.FDdat')
#force data for different laser intensities
force_150mA = np.loadtxt('Brownian_Data/force150.FDdat')
force_200mA = np.loadtxt('Brownian_Data/force200.FDdat')
force_250mA = np.loadtxt('Brownian_Data/force250.FDdat')
force_300mA = np.loadtxt('Brownian_Data/force300.FDdat')
#force data for different laser intensities
force_150mA = np.loadtxt('Brownian_Data/force150.FDdat')
force_200mA = np.loadtxt('Brownian_Data/force200.FDdat')
force_250mA = np.loadtxt('Brownian_Data/force250.FDdat')
force_300mA = np.loadtxt('Brownian_Data/force300.FDdat')












#------------------ Power Spectrum Calculations -------------------#
var = np.var(position[:, 2])*(1E-6)**2 #variance of the position data [m]

alpha = k_B * T / var #trap strength
beta = 3 * np.pi * nu * d 
f_0 = alpha / (2 * np.pi * beta) #fundamental frequency 
P_0 = 2 * k_B * T / (np.pi * alpha * f_0) #fundamental power
#Generating frequency and power spectra:
f = np.logspace(-1, 4, 100) 
P_theory = P_0 * f_0**2 / (f**2 + f_0**2)



#Plotting power spectrum:
plt.figure(figsize=(7, 5))
plt.title('Power Spectrum of 10,000x Silica Solution')
plt.xscale('log')
plt.yscale('log')
plt.xlabel(r'Frequency $f$ [Hz]')
plt.ylabel(r'Power Spectral Density $P(f)$ [m$^{2}$/Hz]')
plt.plot(f, P_theory, color='black', lw=2, label='Theory') #theoretical spectrum
#experimental power spectra for various laser intensities:
plt.scatter( , , color='purple', marker='o', label='Intensity = 150mA') 
plt.scatter( , , color='blue', marker='o', label='Intensity = 200mA') 
plt.scatter( , , color='orange', marker='o', label='Intensity = 250mA') 
plt.scatter( , , color='red', marker='o', label='Intensity = 300mA') 

plt.grid(True, which='both', ls='--', alpha=0.6)
plt.tight_layout()
plt.savefig('Power_Spectrum.png', dpi=300)




