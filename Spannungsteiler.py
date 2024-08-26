import math
import numpy as np

def spannungsteiler(U,R1):
    U1 = 3.3
    R2 = ((1 - (U1/U)) / R1) / (U1/U) 
    return R2

U = 10 #Volt
R1 = 1 #KOhm

print(spannungsteiler(U,R1)) 
print('R_1 / R_2 = '+ str(R1/spannungsteiler(U,R1)) )