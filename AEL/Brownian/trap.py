import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import os



#--------- Global variables/Constants ---------#
k_B = 1.380649E-23   #Boltzmann's constant [J/K]
T = 298              #Temperature [K]
d = 3E-6             #Bead diameter [m]
nu = 8.9E-4          #Viscosity of medium (H2O) [Pa·s]
base_dir = "Brownian_Data"

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
    var_x = np.var(TD[:, 1] / calib_x)
    var_y = np.var(TD[:, 2] / calib_y)
    return var_x, var_y #variances in x and y



#-------- Fitting Theory to Data and Plotting -------#
#theoretical power spectrum function
def power_spectrum(f, P_0, f_0):
    return P_0 * f_0**2 / (f**2 + f_0**2)


#fits and plots power spectrum function to data:
def fit_and_plot(laser_amp, f_data, P_data, variance):
    #theoretical constants
    alpha_theory = k_B * T / variance #trap stiffness [N/m]
    beta = 3 * np.pi * nu * d #drag coefficient [N·s/m]
    f_0_theory = alpha_theory / (2 * np.pi * beta) #corner frequency [Hz]
    P_0_theory = 2 * k_B * T / (np.pi * alpha_theory * f_0_theory) #plateau PSD [m²/Hz]
    f = np.logspace(0, 4, 1000) #frequency range [Hz]

    #curve fitting to get experimental parameters:
    popt, pcov = curve_fit(
        power_spectrum,
        f_data,
        P_data,
        p0=[P_0_theory, f_0_theory],
    )
    P_fit = power_spectrum(f, *popt)
    alpha_exp = popt[1] * 2 * np.pi * beta #experimental trap stiffness [N/m]
    print(variance)
    print(f"$k_Bexp$ at {laser_amp} mA: {alpha_exp * variance / T:.3e} J/K\n")

    
    #plotting:
    plt.figure(figsize=(7, 5))
    plt.title(f"Power Spectrum ({laser_amp} mA Laser Current)")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel(r"Frequency $f$ [Hz]")
    plt.ylabel(r"Power Spectral Density $P(f)$ [m$^2$/Hz]")
    plt.plot(f, P_fit, color="black", lw=2, label="Best-fit Spectrum")
    plt.loglog(f_data, P_data, color="red", marker='o', markersize=0.8,
           label=f"Data {laser_amp} mA")
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"PowSpec_{laser_amp}mA.png", dpi=300)
    plt.close()



#-------- Full Process with Intensities Specified --------#
intensities = [150, 200, 250, 300]

for I in intensities:
    freq_data, pow_x, pow_y= load_FD(I) #getting the power spectral density data
    var_x, var_y = load_TD(I) #getting the x and y variances
    fit_and_plot(I, freq_data, pow_y, var_y) #plotting for specific axis & intensity
