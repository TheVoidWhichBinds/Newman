import numpy as np
import matplotlib.pyplot as plt


#constants:
N = 100
eps = 1

E = np.arange(0,100,1)
R = E/eps

#formula:
S = N*np.log(N/(N-R)) + R*np.log((N-R)/R)

#plotting:
plt.figure()
plt.title('Two-State Entropy')
plt.xlabel('Energy E')
plt.ylabel('Entropy S')
plt.plot(E,S)
plt.savefig('S_v_E')