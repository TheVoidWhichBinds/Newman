import numpy as np

#constants:
a1 = float(15.8)
a2 = float(18.3)
a3 = float(0.714)
a4 = float(23.2)

#a5 function:
def a_5(A,Z):
  if A%2:
    a5 = 0
  elif (A+Z)%2 == 0:
    a5 = float(12.0)
  else:
    a5 = float(-12.0)
  return a5



# a)

A = int(input("The mass number A is: "))
Z = int(input("The atomic number Z is: "))
#
def binding_energy(A,Z):
  a5 = a_5(A,Z)
  B = a1*A - a2*A**(2/3) - a3*(Z**2)/(A**(1/3)) - a4*(A - 2*Z)**2/A + a5/A**(1/2)
  return B

B = binding_energy(A,Z)
print(f"The binding energy of this atom is {B} MeV")



# c)

Z = int(input("The atomic number Z is: "))
#
def stable_atom(Z):
  B_val = np.empty(3*Z - Z, dtype=float)
  A_val = np.arange(Z, 3 * Z)
  # Calculate binding energy for each mass number A
  for i, A in enumerate(A_val):
    B = binding_energy(A, Z)
    B_val[i] = B / A  # Binding energy per nucleon
  # Find the index of the maximum binding energy per nucleon
  index_stable = np.argmax(B_val)
  A_stable = A_val[index_stable]
  #
  return A_stable

print(f"The most stable mass number A for the given atomic number Z of {Z} is {stable_atom(Z)}")
  


