from numpy import float32, int32, pi 
#float32 has to be called otherwise M sees overflow -> float size must be > power of number.


G = float32(6.67E-11)
M = float32(5.97E24)
R = int32(6371E3)
T = float32(input("Period of orbit: "))

h = (G*M*T**2/(4*pi**2))**(1/3) - R

print(f"The orbital hight is {h} meters")
