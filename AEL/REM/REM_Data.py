import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import os
downloads_dir = os.path.expanduser('~/Downloads') 



#-------- data averaging function ----------------------------#
def data_averaging(data, knob_pos, upper_B, lower_B, B_offset):
    #compute B-field from Gaussmeter reading:
    dial_rate = (upper_B - lower_B) / knob_pos
    data[:, 4] = data[:, 1] + B_offset + dial_rate * data[:, 0]
    #group data by knob position (column 0) and average the other columns:
    #(for some reason, # data pts per knob pos inconsistent)
    col0 = data[:, 0]
    change = np.concatenate(([True], col0[1:] != col0[:-1])) #boolean array where knobob position changes
    bounds = np.flatnonzero(change) #indexing where knobob position changes

    #averaging data in each group:
    out = []
    w_list = []

    for s, e in zip(bounds[:-1], bounds[1:]): #grouping indices of same knob position
        rows = data[s:e, :] #all rows with same knob position
        #error analysis & averaging:
        out.append(np.mean(rows, axis=0))
        w_list.append(1/np.std(rows[:, 4], ddof=1)**2) #weight for std error of B-field
    
    data_avg = np.vstack(out) #stacking all averaged rows into array
    w_array = np.array(w_list)
    return data_avg, w_array



#--------- parameters for averaging function -------------------#
#knob_pos = # knob positions moved through (# individual B values)         
#upper_B  = max Gaussmeter reading from screen display    
#lower_B  = initial Gaussmeter reading from screen display 
#B_offset = Gaussmeter reading difference between screen and Arduino input 



#--------- load data ------------------------------------------------#
data1 = pd.read_excel("Bi848.xlsx", sheet_name=0, header=0).to_numpy()
data2 = pd.read_excel("Bi1146.xlsx", sheet_name=0, header=0).to_numpy()
data3 = pd.read_excel("Bi1568.xlsx", sheet_name=0, header=0).to_numpy()



#--------- averaging data sets & generating std error of B-Field ---------#
#inserting data runs from 848 Gauss to ???? Gauss
avg_data = ([
     data_averaging(data1, 500, 1146, 848, 668),
     data_averaging(data2, 700, 1568, 1146, 908), 
     data_averaging(data3, 400, 1822, 1568, 1320)
])

#extracting averaged B-field and pulse counts:
all_avg = np.vstack([out[0] for out in avg_data])
B_field = all_avg[:, 4]
pulses  = all_avg[:, 3]

#finding B-field that results in peak counts:
max_index = np.argmax(pulses)
B_peak = B_field[max_index]
print(f"Peak Pulses B-field: {B_peak:.3f} Gauss")

#extracting error weights and calculating standard error of B-field:
all_weights = np.concatenate([out[1] for out in avg_data])
sigma_B = 1/np.sqrt(np.sum(all_weights, axis=0))
print(f"Std Error of B-field: {sigma_B:.3f} Gauss")




#--------- plotting averaged data ----------#
plt.figure()
plt.title("Relativistic Electron Momentum")
plt.xlabel("Average Magnetic Field (Gauss)")
plt.ylabel("Average Electron Count")
plt.scatter(B_field, pulses, s=6, marker='o', color='purple')
plt.savefig("REM.png", dpi=200)
plt.savefig(os.path.join(downloads_dir, "REM.png"), dpi=200, bbox_inches="tight")

