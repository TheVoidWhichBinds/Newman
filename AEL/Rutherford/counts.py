import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#------------ Global Variables ------------#
# Geometries:
r_i = 2.30 # inner foil radius [cm]
r_o = 2.70 # outer foil radius [cm]
r_1 = (r_i + r_o)/2 # average foil radius [cm]
r_d = 0.48 # detector radius [cm]
A_1 = np.pi*(r_o**2 - r_i**2) # area of gold foil [cm^2]
A_d = np.pi*(r_d**2) # area of detector [cm^2]
X = 7.22 # axial source-foil distance [cm]
R_1 = np.sqrt(X**2 + r_1**2) # distance from source to foil [cm]
theta_1= np.arctan(r_1/X) # source emission angle [radians]
# Nuclear/Material: ------------------------------------------------------------------------------
Z = 79 # gold foil nuclear proton count
t = 2E-4 # gold foil thickness [cm]
z = 2 # scattered particle proton count
e = 3.79E-7 # proton charge [sqrt(cm*MeV)]
rho = 1.932E1 # gold foil density [g/cm^3]
E_s = 4.4 - 0.3*(rho*t) # energy of scattered alpha particles (source energy - foil loss) [MeV]
N_A = 6.02214076E23 # Avogadro's # [1/mol]
A_g = 197.2 # atomic mass of gold [amu][g/mol]
n = rho*N_A*A_1*t/A_g # total # of scattering centers
N_0 = 3# source emission rate [counts/min]             #FAKE NUMBER _ NEEDS TO CHANGE ___
# Constant Calculations: -------------------------------------------------------------------------
Rutherford = (Z*z*e**2)**2/(16*E_s**2) #Rutherford constant
G = Rutherford * (n*(np.pi* r_d**2) / ((X**2 + r_1**2)* r_1**2)) #[cm^-2 MeV^-2]
print(f'G is {G}')




#------------ Downloading Data -------------#
#data= pd.read_excel('Rutherford_Data.xlsx')
#N_2= data[:,2]/5 #[counts/min]
#Y= data[:,1] #foil-detector distance [cm]
N_2= np.array([32,27,29,35,34,40,33,37,32,26,29,21,23,19,10,2])
Y= np.array([19.3,18.1,16.9,15.7,14.5,13.3,12.1,10.9,9.7,8.5,7.3,6.1,4.9,3.7,2.5,1.3])




#------------- Theoretical & Experimental Functions -------------#
def angle_theory():
    Y_t = np.linspace(1,20,100)
    theta_2 = np.pi/2 - np.arctan(Y_t/r_1)
    theta = theta_1 + theta_2
    fY_t = np.cos(theta_2) * (np.sin(theta_2))**2 / (np.sin(theta/2))**4
    return Y_t, fY_t

def cross_theory():
    theta = np.linspace(0.1, 0.9, 1000) #[radians]
    Xsec_theory = Rutherford / (np.sin(theta/2))**4
    return theta, Xsec_theory

def cross_exp():
    theta_2 = np.arctan(r_1/Y)
    theta_exp = theta_1 + theta_2
    Xsec_exp =  (N_2 * R_1**2 * r_1**2 / 
                (n * N_0 * A_d * np.cos(theta_2)*(np.sin(theta_2))**2)
    )
    return theta_exp, Xsec_exp
    



#------------- Plotting -----------------#
# Theoretical Y_t vs f(Y_t):
def plotting():
    # Calling functions and saving x and y axis variables:
    Y, fY = angle_theory()
    theta, Xsec_theory = cross_theory()
    theta_exp, Xsec_exp = cross_exp()
    
    
    plt.figure()
    plt.title('Scattering Angular Dependence')
    plt.xlabel('Foil-Detector Distance Y [cm]')
    plt.ylabel('Angular Dependence of Count Rate f(Y)')
    plt.plot(Y, fY) #
    plt.savefig('f(Y).png')
    #plt.show()

    # N2 as a Func of Y:
    plt.figure()
    plt.title('Rutherford Nucleus Scattering')
    plt.xlabel('Scattering Foil-Detector Distance Y [cm]')
    plt.ylabel(r'Count Rate $N_2$ [counts/min]')
    plt.plot(Y, N_0*G*fY, label='Theory') # Y, N_2
    plt.scatter(Y, N_2, color='purple', label='Data')
    plt.legend()
    plt.savefig('N2.png')
    #plt.show()

    # Theoretical & experimental differential scattering cross-section:
    plt.figure()
    plt.title('Differential Scattering Cross-Section') 
    plt.xlabel(r'Scattering Angle $\theta$ [Radians]')
    plt.ylabel(r'Differential Cross Section $\frac{d\sigma}{d\Omega}$ [UNITS]')
    plt.yscale('log')
    plt.plot(theta, Xsec_theory, label='Theory') #
    plt.scatter(theta_exp, Xsec_exp, color='purple', label='Experimental')
    plt.legend()
    plt.savefig('Rutherford.png')
    plt.show()


plotting()