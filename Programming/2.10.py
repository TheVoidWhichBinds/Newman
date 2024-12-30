from numpy import empty, size

# a)

A = int(input("The mass number A is: "))
Z = int(input("The atomic number Z is: "))
#    
if A%2 != 0:
  a5 = 0
elif (A+Z)%2 == 0:
  a5 = float(12.0)
else:
  a5 = float(-12.0)
#
a1 = float(15.8)
a2 = float(18.3)
a3 = float(0.714)
a4 = float(23.2)
#
B = a1*A - a2*A**(2/3) - a3*(Z**2)/(A**(1/3)) - a4*(A - 2*Z)**2/A + a5/A**(1/2)

print(f"The binding energy of this atom is {B} MeV")


# c)

Z = int(input("The atomic number Z is: "))
def stable_atom(Z):
  #
  E_per_nucleon = empty(size(range(Z,3*Z)))
  for A,i in range(Z, 3*Z):
    B = a1*A - a2*A**(2/3) - a3*(Z**2)/(A**(1/3)) - a4*(A - 2*Z)**2/A + a5/A**(1/2)
    E_per_nucleon[i] = B/A
  #
  A_stable  


