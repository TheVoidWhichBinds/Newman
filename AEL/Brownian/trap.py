import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import os
downloads_dir = os.path.expanduser('~/Downloads') 




#--------- Global variables/Constants ---------#
k_B = 1.380649E-23   #Boltzmann's constant [J/K]
T = 298              #Temperature [K]
d = 3E-6             #Bead diameter [m]
nu = 8.9E-4          #Viscosity of medium (H2O) [Pa·s]
base_dir = "Brownian_Data"
#
#QPD conversion factors: given in V/µm -> convert to V/m
calib_x = 579e-3 * 1e6   #0.579 V/µm -> [V/m]
calib_y = 488e-3 * 1e6   #0.488 V/µm -> [V/m]




#------------------- Data-Loading Functions -------------------#
#.FDdat files have commas after 2nd column that must be removed:
def strip_comma(x): 
    if isinstance(x, bytes):
        x = x.decode()
    return float(x.replace(",", ""))


#loads force data, converts it to correct units:
def load_FD(laser_amp):
    """open Brownian_Data/force{laser_amp}.FDdat (frequency-domain)"""
    path = os.path.join(base_dir, f"force{laser_amp}.FDdat")
    FD = np.genfromtxt(
        path,
        comments="#",
        skip_header=4,
        autostrip=True,
        converters={1: strip_comma},   #col 1 may have commas
    )
    freq_data = FD[:, 0] #Frequency [Hz]
    pow_x = FD[:, 1] / (calib_x**2) #PSD x [m²/Hz]
    pow_y = FD[:, 2] / (calib_y**2) #PSD y [m²/Hz]
    return freq_data, pow_x, pow_y #frequency, power spectral densities in x and y


#loads position data, takes the variance:
def load_TD(laser_amp): 
    """open Brownian_Data/force{laser_amp}.TDdat (time-domain) and return x,y variances"""
    path = os.path.join(base_dir, f"force{laser_amp}.TDdat")
    TD = np.genfromtxt(
        path,
        comments="#",
        skip_header=4,
        autostrip=True,
    )
    time = np.var(TD[:, 0])
    var_x = np.var(TD[:, 1] / calib_x)
    var_y = np.var(TD[:, 2] / calib_y)
    return time, var_x, var_y #variances in x and y




#-------- Fitting Theory to Data and Plotting Functions -------#
#theoretical power spectrum function
def power_spectrum(f, P_0, f_0):
    return P_0 * f_0**2 / (f**2 + f_0**2)


#fits and plots power spectrum function to data:
def PSD(laser_amp, f_data, P_data, variance):
    #theoretical constants
    alpha_theory = k_B * T / variance #trap stiffness [N/m]
    beta = 3 * np.pi * nu * d #drag coefficient [N·s/m]
    f_0_theory = alpha_theory / (2 * np.pi * beta) #corner frequency [Hz]
    P_0_theory = 2 * k_B * T / (np.pi * alpha_theory * f_0_theory) #plateau PSD [m²/Hz]
    f = np.logspace(0, 4, 1000) #frequency range [Hz]
    #
    # Curve fitting to get experimental parameters:
    popt, pcov = curve_fit(
        power_spectrum,
        f_data,
        P_data,
        p0=[P_0_theory, f_0_theory],
    )
    P_fit = power_spectrum(f, *popt)
    alpha_exp = popt[1] * 2 * np.pi * beta #experimental trap stiffness [N/m]
    print(f"$alpha$ at {laser_amp} mA: {alpha_exp:.3e} N/m")
    print(f"$k_Bex$ at {laser_amp} mA: {alpha_exp * variance / T:.3e} J/K\n")
    #
    # Plotting:
    plt.figure(figsize=(7, 5))
    plt.title(f"Power Spectrum ({laser_amp} mA Laser Current)")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel(r"Frequency $f$ [Hz]")
    plt.ylabel(r"Power Spectral Density $P(f)$")
    plt.plot(f, P_fit, color="black", lw=2, label="Best-fit Spectrum")
    plt.scatter(f_data, P_data, color="red", marker='o', s=1,
           label=f"Data {laser_amp} mA")
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"PowSpec_{laser_amp}mA.png", dpi=300)
    plt.savefig(os.path.join(downloads_dir, "PSD300.png"), dpi=200, bbox_inches="tight")
    plt.close()




#--------- PSD Plotting ---------#
intensities = [150, 200, 250, 300]
#
for I in intensities:
    freq_data, pow_x, pow_y= load_FD(I) #getting the power spectral density data
    time, var_x, var_y = load_TD(I) #getting the x and y variances
    PSD(I, freq_data, pow_x, var_x) #plotting for specific axis & intensity




#------ Trap Stiffness vs. Laser Intensity Plotting ------#
I = np.array(intensities) #laser intensities [mA]
#Experimental trap stiffnesses [N/m]:
alpha_x = np.array([
    9.924e-08,   # 150 mA
    -1.042e-07,  # 200 mA
    1.405e-07,   # 250 mA
    1.169e-07    # 300 mA
])
alpha_y = np.array([
    5.054e-08,   # 150 mA
    3.046e-08,   # 200 mA
    3.137e-08,   # 250 mA
    3.329e-08    # 300 mA
])

# Plots:
plt.figure(figsize=(7, 5))
plt.title("Trap Stiffness vs. Laser Intensity")
plt.xlabel("Laser Intensity [mA]")
plt.ylabel("Trap Stiffness $\\alpha$ [N/m]")
plt.plot(I, alpha_x, '-o', markersize=8, color='blue', label='X-axis')
plt.plot(I, alpha_y, '-o', markersize=8, color='orange', label='Y-axis')
plt.legend(loc='lower right')
plt.grid(True, which="both", ls="--", alpha=0.6)
plt.tight_layout()
plt.savefig("Alpha_Intensity.png", dpi=300)
plt.savefig(os.path.join(downloads_dir, "alpha.png"), dpi=200, bbox_inches="tight")