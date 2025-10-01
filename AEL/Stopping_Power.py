import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


E_r = 0.511   #m_0*c^2       [MeV]
I = 86E-6     #              [MeV]
C = 9.234e-05 #0.5*rho*K*Z/A [MeV/cm]
E_max = 1.064     #          [MeV]
s_min = np.pi*1.9 #          [cm]
s_max = 50 #          [cm]


def beta_func(E):
    beta = np.sqrt(1 - (E_r/E)**2)
    return beta


def gamma_func(E):
    gamma = E/E_r
    return gamma


def dE_ds(E):
    b = beta_func(E)
    g = gamma_func(E)
    
    E_deriv= (C/(b**2))*(
    np.log((E_r*(b**2)*(g**2) * (E_r*(g-1.0)/2.0)) / (I**2))  # E_r=0.511 MeV, I in MeV
    + (1.0 - b**2)
    - ((2.0*g - 1.0)/g**2)*np.log(2.0)
    + 0.125*((g-1.0)/g)**2)
    return  E_deriv




# E_loss = solve_ivp(
#     dE_ds, 
#     t_span=(0, s_max), 
#     y0=[E_max], 
#     t_eval = np.linspace(0, s_max, 200))

E_range = np.linspace(1.064, 10.0, 400)   # 400 points
S = dE_ds(E_range)                         # your function is vectorized
plt.figure()
plt.plot(E_range, S)                       # or: plt.plot(E_range, S, marker='.')
plt.xlabel("Energy [MeV]")
plt.ylabel("Linear Stopping Power [MeV/cm]")
plt.title("Relativistic Stopping Power")
plt.savefig("Stopping_Power.png", dpi=200, bbox_inches="tight")



# plt.figure()
# plt.plot(E_loss.t, E_loss.y[0])
# plt.ylabel("Total Relativistic Energy [MeV]")
# plt.xlabel(" Distance [cm]")
# plt.title("Relativistic Electron Energy Loss")
# plt.savefig("Rel_Energy_Loss")
