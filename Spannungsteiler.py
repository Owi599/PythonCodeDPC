import math
import numpy as np

def spannungsteiler(U,R1):
    U1 = 3.3
    R2 = ((U-U1)*R1)/U1 
    return R2

U = 12 #Volt
R1 = 100000#Ohm

print(spannungsteiler(U,R1)) 
print('R_1 / R_2 = '+ str(R1/spannungsteiler(U,R1)) )
