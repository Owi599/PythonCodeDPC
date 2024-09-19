import math
import numpy as np

def spannungsteiler(U,R1):
    U1 = 10
    R2 = ((U-U1)*R1)/U1 
    return R2

U = 48 #Volt
R1 = 3000#Ohm

print(spannungsteiler(U,R1)) 
print('R_1 / R_2 = '+ str(R1/spannungsteiler(U,R1)) )
