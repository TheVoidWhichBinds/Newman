import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import os
downloads_dir = os.path.expanduser('~/Downloads') 

#---------- constants ----------#
E_r = 0.511 #m_0*c^2 [MeV]
I = 8.57E-5 #[MeV]
C = 9.24E-5 #0.5*rho*K*Z/A [MeV/cm]
E_max = 1.48 #[MeV] initial energy of electron
s_avg = np.pi*2.5 #[cm] average arc length to detector
s_max = 50 #[cm] arbitrary large distance for energy loss plotting


#---------- stopping power functions ----------#
#classic relativistic beta (v/c) solved in terms of total energy E and rest energy E_r:
def beta_func(E): 
    beta = np.sqrt(1 - (E_r/E)**2)
    return beta

#classic relativistic gamma (1/sqrt(1-beta^2)) solved in terms of total energy E and rest energy E_r
def gamma_func(E): 
    gamma = E/E_r
    return gamma

#stopping power function dE/ds in MeV/cm
def stopping_rate(E):
    b = beta_func(E)
    g = gamma_func(E)
    
    E_deriv= (C/(b**2))*(
    np.log((E_r*(b**2)*(g**2) * (E_r*(g-1.0)/2.0)) / (I**2))  # E_r=0.511 MeV, I in MeV
    + (1.0 - b**2)
    - ((2.0*g - 1.0)/g**2)*np.log(2.0)
    + 0.125*((g-1.0)/g)**2)
    return  E_deriv

#---------- solving ODE for E as a function of distance traveled s ----------#
dE_ds = lambda s, E: -stopping_rate(E) #puts stopping rate in form for ODE solver
E_loss = solve_ivp( #ODE solver
    dE_ds, 
    t_span=(0, s_max), 
    y0=[E_max], 
    t_eval = np.linspace(0, s_max, 200))


#---------- plotting stopping rate [MeV/cm] ----------#
E_range = np.linspace(0.7, 10.0, 400) #arbitrary range of energies for plotting
S = stopping_rate(E_range)
plt.figure()
plt.plot(E_range, S)
plt.xlabel("Energy [MeV]")
plt.ylabel("Linear Stopping Power [MeV/cm]")
plt.title("Relativistic Stopping Power")
plt.savefig("Stopping_Power.png", dpi=200, bbox_inches="tight")
#plt.savefig(os.path.join(downloads_dir, "Stopping_Power.png"), dpi=200, bbox_inches="tight")

#---------- plotting E as a func of distance traveled -----------#
plt.figure()
plt.plot(E_loss.t, E_loss.y[0])
plt.ylabel("Total Relativistic Energy [MeV]")
plt.xlabel(" Distance [cm]")
plt.title("Relativistic Electron Energy Loss")
plt.savefig("Rel_Energy_Loss")
#plt.savefig(os.path.join(downloads_dir, "Rel_Energy_Loss.png"), dpi=200, bbox_inches="tight")

#---------- finds E_det from trajectory arc length s ----------#
#given E_loss plot x axis (distance s), and target distance s, find index of closest distance in s_range
def detector_energy(s_range, s): 
    i = np.searchsorted(s_range, s)
    i = np.clip(i, 1, len(s_range)-1)
    return i-1 if s - s_range[i-1] <= s_range[i] - s else i

s_index = detector_energy(E_loss.t, s_avg) 
E_det = E_loss.y[0][s_index] #energy at detector corresponding to average arc length s_avg
print(f"Average energy at detector: {E_det:.3f} MeV")