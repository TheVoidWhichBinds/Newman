import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#------------ Global Variables ------------#
#Geometries:
r_i= 2.30 #[cm]
r_o= 2.70 #[cm]
r_1= (r_i + r_o)/2 #average foil radius [cm]
r_d= 0.48 #detector radius [cm]
X= 7.22 #[cm]
#Nuclear/Material:
Z= 79 #gold foil nuclear proton count
t= 2E-4 #gold foil thickness [cm]
z= 2 #scattered particle proton count
e= 0.303 #proton charge [dimensionless]
rho= 1.932E4 #gold foil density [mg/cm^3]
E_s= 4.4 - 0.3*(rho*t) #energy of scattered alpha particles (source energy - foil loss) [MeV]
N_A= 6.02214076E23 #Avogadro's # [1/mol]
A_g= 197.2 #atomic mass of gold [amu]
N_0= 100# source emission rate [counts/min].             #FAKE NUMBER _ NEEDS TO CHANGE ___
#Constant Calculations:
R= (Z*z*e**2)**2/(16*E_s**2) #Rutherford constant
G= R* ((rho* N_A* np.pi(r_o**2 - r_i**2)* t)*(np.pi* r_d**2) / (A_g* (X**2 + r_1**2)* r_1**2)) #[cm^-2 MeV^-2]
 


#------------ Downloading Data -------------#
data= pd.read_excel('Rutherford_Data.xlsx')
N_2= data[:,2]/5 #[counts/min]
Y= data[:,1] #foil-detector distance [cm]



#------------- Theoretical Calculations -------------#
def theory():
    Y_t= np.linspace(1,20,100)
    theta_1= np.arctan(r_1/X)
    theta_2= np.pi/2 - np.arctan(Y_t/r_1)
    theta= theta_1 + theta_2
    fY_ = np.cos(theta_2) * (np.sin(theta_2))**2 / (np.sin(theta/2))**4
    return Y_t, fY_t



#------------- Plotting -----------------#
#Theoretical Y_t vs f(Y_t):
plt.figure()
plt.title('')
plt.xlabel('Foil-Detector Distance Y [cm]')
plt.ylabel('Angular Dependence of Count Rate f(Y)')
Y_t, fY_t= theory()
plt.plot(Y_t, fY_t)
plt.savefig('f(Y).png')
plt.show()

#N2 as a Func of Y:
plt.figure()
plt.title('Scattering Angle')
plt.xlabel('Scattering Foil-Detector Distance Y [cm]')
plt.ylabel(r'Count Rate $N_2$ [counts/min]')
plt.scatter(Y, N_2, color='purple', label='Data')
plt.plot(Y_t, N_0*G*fY_t, color='blue', label='Theory') #theoretical plot scaled to be Y vs N_2
plt.legend()
plt.savefig('N2.png')
plt.show()
