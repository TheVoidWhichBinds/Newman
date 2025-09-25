import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

R_0   = 1.0E-24   #4*pi*r_0^2[cm^2]
E_r   = 0.511     #m_0*c^2   [MeV]
n     = 3.88E20   #NZ        [#/cm^3]
I     = 86E-6     #          [MeV]
E_max = 1.064     #          [MeV]
s_min = np.pi*1.9 #          [cm]
s_max = np.pi*3.1 #          [cm]


def Beta_func(E):
    Beta = np.sqrt(1 - (E_r/E)**2)
    return Beta

def dE_ds(s,E):
    b = Beta_func(E)
    return (R_0*E_r*n/(b*b) * np.log(b*((E+E_r)/I)*np.sqrt(E/E_r)) - 0.5*b*b)

E_loss = solve_ivp(
    dE_ds, 
    t_span=(0, 2), 
    y0=[E_max], 
    t_eval = np.linspace(0, 2, 200))


plt.figure()
plt.plot(E_loss.t, E_loss.y[0])
plt.xlabel("Path length s [cm]")
plt.ylabel("Total Relativistic Energy E(s) [MeV]")
plt.title("Energy vs Distance")
plt.savefig("Energy_Loss")
