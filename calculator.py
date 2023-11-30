import numpy as np
import math # python math library
import matplotlib # pythom plotting library
import sympy as sp
from sympy import cos, sin
from sympy import symbols as sym
from sympy import Matrix as mat
matplotlib.use("TkAgg")
import matplotlib.animation as animation # python animation library
import numpy as np # python array manipulation library
from gekko import GEKKO #a Python library for machine learning and optimization

def get_phi_R(Phi_D):
    Phi_R = Phi_D*np.pi/180    
    
    return Phi_R

Angle = get_phi_R(20)
#print(Angle)

"""
m = GEKKO(remote=False)

#Parameters
mc  = m.Param(value=1.2)  #cart mass
m1  = m.Param(value=.5)   #link 1 mass
m2  = m.Param(value=.3)   #link 2 mass
L1  = m.Param(value=.3)   #link 1 length
LC1 = m.Param(value=.3)   #link 1 Center Mass pos
L2  = m.Param(value=.3)   #link 1 length
LC2 = m.Param(value=.3)   #link 1 Center Mass pos
I1  = m.Param(value=.01)  #link 1 Moment of Inertia
I2  = m.Param(value=.01)  #link 2 Moment of Inertia
g   = m.Const(value=9.81) #gravity
Bc  = m.Const(value=.5)   #cart friction
B1  = m.Const(value=.001) #link 1 friction
B2  = m.Const(value=.001) #link 2 friction

TF = m.FV(12,lb=2,ub=25); TF.STATUS = 1 

#Manipulative Variable 
u = m.MV(lb=-100,ub=100); u.STATUS = 1

#State Variables
x, xdot, q1, q1dot, q2, q2dot = m.Array(m.Var, 6)

#Intermediates
h1 = m.Intermediate(mc + m1 + m2)
h2 = m.Intermediate(m1*LC1 + m2*L1)
h3 = m.Intermediate(m2*LC2)
h4 = m.Intermediate(m1*LC1**2 + m2*L1**2 + I1)
h5 = m.Intermediate(m2*LC2*L1)
h6 = m.Intermediate(m2*LC2**2 + I2)
h7 = m.Intermediate(m1*LC1*g + m2*L1*g)
h8 = m.Intermediate(m2*LC2*g)

M = np.array([[h1, h2*m.cos(q1), h3*m.cos(q2)],
              [h2*m.cos(q1), h4, h5*m.cos(q1-q2)],
              [h3*m.cos(q2), h5*m.cos(q1-q2), h6]])
C = np.array([[Bc, -h2*q1dot*m.sin(q1), -h3*q2dot*m.sin(q2)],
              [0, B1+B2, h5*q2dot*m.sin(q1-q2)-B2],
              [0, -h5*q1dot*m.sin(q1-q2)-B2, B2]])

G = np.array([0, -h7*m.sin(q1), -h8*m.sin(q2)])
U = np.array([u, 0, 0])
DQ = np.array([xdot, q1dot, q2dot])
CDQ = C@DQ
b = np.array([xdot.dt()/TF, q1dot.dt()/TF, q2dot.dt()/TF])
Mb = M@b
""" 

mc , m1 , m2 , g, Bc, B1, B2, L1, L2, LC1, LC2, I1, I2, x, xdot, q1, q1dot, q2, q2dot, u, TF = sym('mc m1 m2 g Bc B1 B2 L1 L2 LC1 LC2 I1 I2 x xdot q1 q1dot q2 q2dot u TF')

M_sym = mat([
            [(mc +m1 +m2), (m1*LC1 + m2*L1)*cos(q1), m2*LC2*cos(q2)],
            [(m1*LC1 + m2*L1)*cos(q1), (m1*LC1**2 + m2*L1**2 + I1), m2*LC2*L1*cos(q1-q2)],
            [m2*LC2*cos(q2), m2*LC2*L1*cos(q1-q2), (m2*LC2**2 + I2)]
        ])

print(M_sym)
