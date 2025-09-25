import numpy as np

R_0 = 1.0E-24 #4*pi*r_0^2 [cm^2]
E_r = 0.511 #m_0*c^2 [MeV]
n = 3.88E20 #NZ [#/cm^3]
I = 86E-6 # [MeV]
E = 1.064 # [MeV]

def Beta_func(E):
  Beta = (1 - (E_r/E)**2)
  return Beta
Beta = Beta_func(E)


def E_loss_func(E):
  E_loss = R_0*E_r*n/Beta * ( np.ln(Beta*((E+E_r)/I)*np.sqrt(E/E_r)) - (Beta**2)/2 )
  return E_loss

E_loss = E_loss_func(E)
