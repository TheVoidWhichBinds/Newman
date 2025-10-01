import matplotlib.pyplot as plt
import numpy as np 

data = np.loadtxt("REM_test.txt", delimiter=",")




plt.figure()
plt.xlabel("Magnetic Field (Gauss)")
plt.ylabel("Electron Count")
plt.scatter(B_field, pulses, 'o', color = 'purple')





