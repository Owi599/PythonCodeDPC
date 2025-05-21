import math
import numpy as np

def spannungsteiler(U,R1):
    U1 = 3.3 #Volt
    R2 = ((U-U1)*R1)/U1 
    return R2

U = 12 #Volt
R1 = 168e3#Ohm

print(spannungsteiler(U,R1)/1000,'kOhm') 
print('R_1 / R_2 = '+ str(R1/spannungsteiler(U,R1)) )


def minimaler_widerstand(U):
    I = 250e-3 / U # milli Watt/ volt = milli Ampere I = P/U
    Rmin  = U / I  # volt / milli Ampere = KOhm
    return Rmin

minimaler_widerstand = minimaler_widerstand(12)
print('Minimaler Widerstand: ' + str(minimaler_widerstand) + ' KOhm')