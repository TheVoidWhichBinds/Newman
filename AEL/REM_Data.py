import matplotlib.pyplot as plt
import numpy as np 


num_fixed_B = 25  #number of data points collected at a fixed magnetic field
num_B_val = 28  #number of different magnetic field values scanned over
B_offset = 500 #B field data saved in .txt with fixed offset 

data = np.loadtxt("REM_test.txt", delimiter=",") 
data_avg = np.empty((num_B_val, 4))


for i in range(num_B_val):
    rows = data[i*num_fixed_B:(i+1)*num_fixed_B, :] #slicing rows i*num_fixed_B : (i+1)*num_fixed_B, all columns
    data_avg[i, :] = np.mean(rows, axis=0) #averaging over rows


#[0] column = index
B_field = data_avg[:,1] + B_offset #[1] column = B field [Gauss]
#[2] column = null
pulses = data_avg[:, 3] #[3] column = pulse count


plt.figure()
plt.title("Relativistic Electron Momentum")
plt.xlabel("Average Magnetic Field (Gauss)")
plt.ylabel("Average Electron Count")
plt.scatter(B_field, pulses, marker='o', color = 'purple')
plt.savefig("REM.png", dpi = 200)






