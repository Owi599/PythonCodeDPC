import numpy as np
import math




def get_phi_R(Phi_D):
    Phi_R = Phi_D*np.pi/180    
    
    return Phi_R

Angle = get_phi_R(20)
print(Angle)
