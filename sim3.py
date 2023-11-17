import numpy as np
import sympy as sp
from sympy import symbols as sym
from sympy import sin as sin
from sympy import cos as cos
from sympy import diff as d
from sympy import Matrix as mat
from sympy import Function
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
from matplotlib.animation import PillowWriter
from scipy.integrate import odeint

# Constants
yc = 0
g = sym('g')


#define constant symbols
mc , m1 , m2  = sym('mc m1 m2')
l1 , l2 = sym('l1 l2')
M = mc + m1 + m2

#define time-varying symbols
t = sym('t')
xc = sym(r'\x_c', cls=sp.Function)(t)
theta1 = sym(r'\theta_1', cls=sp.Function)(t)
theta2 = sym(r'\theta_2', cls=sp.Function)(t)

#Position variables
x1 = xc + l1*sin(theta1)
x2 = x1 + l2*sin(theta2)
y1 = - l1*cos(theta1)
y2 = y1 - l2*cos(theta2)

#Derivatives
dxc = d(xc,t)
ddxc = d(dxc,t)
dtheta1 = d(theta1,t)
dtheta2 = d(theta2,t)
ddtheta1 = d(theta1,t)
ddtheta2 = d(theta2,t)

F = M*ddxc


#kenetic energy
Tc = 1/2*M*(d(xc,t)**2)
T1 = 1/2*m1*(d(x1,t)**2 + d(y1,t)**2)
T2 = 1/2*m2*(d(x2,t)**2 + d(y2,t)**2)
T = Tc + T1 + T2

#potential energy
Vc = 0
V1 = m1*g*y1
V2 = m2*g*y2
V = Vc + V1 + V2

#Lagrangian
L = T - V

#print('Lagrangian:', L.simplify())

#Lagrange equation for xc
LE1 = d(L,xc) - d(d(L,dxc),t).simplify()
#print('Lagrange equation for xc:', eq1.simplify())
#Lagrange equation for theta1
LE2 = d(L,theta1) - d(d(L,dtheta1),t).simplify()
#print('Lagrange equation for theta1:', eq2.simplify())
#Lagrange equation for theta2
LE3 = d(L,theta2) - d(d(L,dtheta2),t).simplify()
#print('Lagrange equation for theta2:', eq3.simplify())

sol1 = sp.solveset(LE1,ddxc)
sol2 = sp.solveset(LE2,ddtheta1)
sol3 = sp.solveset(LE3,ddtheta2)

#print('ddxc= ', sol1)
#print('ddtheta1:', sol2)
#print('ddtheta2:', sol3)


#z-substuitions
dzcdt_f = sp.lambdify((t,g,m1,m2,mc,l1,l2,xc,theta1,theta2,dxc,dtheta1,dtheta2),sol1[ddxc])
dz1dt_f = sp.lambdify((t,g,m1,m2,mc,l1,l2,xc,theta1,theta2,dxc,dtheta1,dtheta2),sol2[ddtheta1])
dz2dt_f = sp.lambdify((t,g,m1,m2,mc,l1,l2,xc,theta1,theta2,dxc,dtheta1,dtheta2),sol3[ddtheta2])
dxc_f = sp.lambdify((xc),xc)
dtheta1_f = sp.lambdify((theta1),theta1)
dtheta2_f = sp.lambdify((theta2),theta2)

def dSdt(S, t, g, mc, m1, m2, l1, l2):
    xc, zc, theta1, z1, theta2, z2 = S
    return[
            dxc_f(zc),
            dzcdt_f(t,g,m1,m2,mc,l1,l2,xc,theta1,theta2,zc,z1,z2),
            dtheta1_f(z1),
            dz1dt_f(t,g,m1,m2,mc,l1,l2,xc,theta1,theta2,zc,z1,z2),
            dtheta2_f(z2),
            dz2dt_f(t,g,m1,m2,mc,l1,l2,xc,theta1,theta2,zc,z1,z2)
            ]

#initial conditions
t = np.linspace(0,40,1001)
g = 9.81
mc = 1
m1 = .5
m2 = .5
l1 = 1
l2 = 1
ans = odeint(dSdt, y0=[0,0,0,0,0,0], t=t, args=(g,mc,m1,m2,l1,l2))

print(ans.T)
