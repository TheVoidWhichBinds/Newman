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
def strip_comma(x):
    # Works whether x is bytes or string
    if isinstance(x, bytes):
        x = x.decode()
    return float(x.replace(',', ''))

pow150 = np.genfromtxt(
    'Brownian_Data/force150.FDdat',
    comments='#',
    skip_header=4,
    autostrip=True,
    converters={1: strip_comma},  # apply to column 1
)

pow200 = np.genfromtxt(
    'Brownian_Data/force200.FDdat',
    comments='#',
    skip_header=4,
    autostrip=True,
    converters={1: strip_comma},  # apply to column 1
)

pow250 = np.genfromtxt(
    'Brownian_Data/force250.FDdat',
    comments='#',
    skip_header=4,
    autostrip=True,
    converters={1: strip_comma},  # apply to column 1
)

pow300 = np.genfromtxt(
    'Brownian_Data/force300.FDdat',
    comments='#',
    skip_header=4,
    autostrip=True,
    converters={1: strip_comma},  # apply to column 1
)



#------------------ Power Spectrum Calculations -------------------#
#experimental data:
var = np.var(position[:, 2])*(1E-6)**2 #variance of the position data [m]
# QPD conversion factors: given in V/µm -> convert to V/m
calib_x = 579e-3 * 1e6  # 0.579 V/µm -> 5.79e5 V/m
calib_y = 488e-3 * 1e6  # 0.488 V/µm -> 4.88e5 V/m

# frequencies
f150 = pow150[:, 0]
f200 = pow200[:, 0]
f250 = pow250[:, 0]
f300 = pow300[:, 0]

# convert PSD from V^2/Hz -> m^2/Hz 
pow150_x = pow150[:, 1] / (calib_x**2)
pow150_y = pow150[:, 2] / (calib_y**2)

pow200_x = pow200[:, 1] / (calib_x**2)
pow200_y = pow200[:, 2] / (calib_y**2)

pow250_x = pow250[:, 1] / (calib_x**2)
pow250_y = pow250[:, 2] / (calib_y**2)

pow300_x = pow300[:, 1] / (calib_x**2)
pow300_y = pow300[:, 2] / (calib_y**2)

#theoretical constants:
alpha = k_B * T / var #trap strength
beta = 3 * np.pi * nu * d 
f_0 = alpha / (2 * np.pi * beta) #fundamental frequency 
P_0 = 2 * k_B * T / (np.pi * alpha * f_0) #fundamental power
#Generating frequency and theoretical power spectra:
f = np.logspace(0, 4, 100) 
P_theory = P_0 * f_0**2 / (f**2 + f_0**2)



#------------------------ Plotting ---------------------------#
#Plotting power spectrum:
plt.figure(figsize=(7, 5))
plt.title('Power Spectrum of 10,000x Silica Solution')
plt.xscale('log')
plt.yscale('log')
plt.xlabel(r'Frequency $f$ [Hz]')
plt.ylabel(r'Power Spectral Density $P(f)$ [m$^{2}$/Hz]')

#plt.plot(f, P_theory, color='black', lw=2, label='Theory') #theoretical spectrum
#experimental power spectra for various laser intensities:
plt.scatter(f150, pow150_x, color='purple', marker='o', s=0.8, label='Intensity = 150mA (x-axis)') 
plt.loglog(f300, pow300_y, 'o', color='red', markersize=0.8, label='Intensity = 300 mA (y-axis)')
#plt.scatter(f200, pow200_y, color='blue', marker='x', s=7, label='Intensity = 200mA (y-axis)')



plt.grid(True, which='both', ls='--', alpha=0.6)
plt.tight_layout()
plt.savefig('Power_Spectrum.png', dpi=300)




