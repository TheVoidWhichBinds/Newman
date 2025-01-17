import numpy as np
import matplotlib.pyplot as plt

#constants:
z = 3 #[meters]
lam = 1 #[meter]
res = 1E8 #number of x points

#adjustable "constants":
N = 100 #Guass-Legendre number of anchor points
x = np.linspace(-5,5,N)
u = x * np.sqrt(2/(lam*z))

#imported Gauss-Legendre quadrature function to calculate the adjusted weights and x points:
def gaussxwab(N, a, b): 
    """
    Calculates the sample points and weights for Gauss-Legendre quadrature.

    Parameters:
    N: Number of sample points.
    a: Lower limit of integration.
    b: Upper limit of integration.

    Returns:
    x: Sample points.
    w: Weights.
    """

    x, w = np.polynomial.legendre.leggauss(N)
    x = 0.5 * (b - a) * x + 0.5 * (a + b)
    w = 0.5 * (b - a) * w
    return x, w

def Gauss_Integral(N):
    tp,wp = gaussxwab(N, np.zeros(np.size(u)), u)
    C = 0 #initializing cosine integral
    S = 0 #initializing sine integral
    for i in range(N):
        C += wp * np.cos(0.5*np.pi * tp**2)
        S += wp * np.sin(0.5*np.pi * tp**2)
    return C, S

C, S = Gauss_Integral(N)
intensity_ratio = (1/8) * ((2*C + 1)**2  + (2*S + 1)**2)


#plotting:
plt.figure()
plt.title('Near-Field Diffraction Intensity')
plt.xlabel('x-Distance from Diffraction Point [meters]')
plt.ylabel(f'Intensity Ratio $I/I_0$')
plt.plot(x, intensity_ratio, 'm')
plt.savefig('Diffraction Intensity')
