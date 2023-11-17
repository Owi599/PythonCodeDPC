import numpy as np
import sympy as sp
import math as m
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
mc , m1 , m2 , M = sym('mc m1 m2 M')
l1 , l2 = sym('l1 l2')
M = mc + m1 + m2
F = sym('F')

#define time-varying symbols
t = sym('t')
xc, x1 ,x2 = sym(r'\x_c, \x_1, \x_2', cls=sp.Function)
yc, y1 ,y2 = sym(r'\y_c, \y_1, \y_2', cls=sp.Function)
dxc , dx1 , dx2 = sym(r'\dot{\x}_c, \dot{\x}_1, \dot{\x}_2', cls=sp.Function)
dy1 , dy2 = sym(r'\dot{\y}_1, \dot{\y}_2', cls=sp.Function)
ddxc , ddx1 , ddx2 = sym(r'\ddot{\x}_c, \ddot{\x}_1, \ddot{\x}_2', cls=sp.Function)
ddy1 , ddy2 = sym(r'\ddot{\y}_1, \ddot{\y}_2', cls=sp.Function)
theta1 = sym(r'\theta_1', cls=sp.Function)
theta2 = sym(r'\theta_2', cls=sp.Function)
dtheta1 = sym(r'\dot{\theta}_1', cls=sp.Function)
dtheta2 = sym(r'\dot{\theta}_2', cls=sp.Function)
ddtheta1 = sym(r'\ddot{\theta}_1', cls=sp.Function)
ddtheta2 = sym(r'\ddot{\theta}_2', cls=sp.Function)

#define functions explicitly
xc = xc(t)
x1 = x1(t) 
x2 = x2(t)
y1 = y1(t)
y2 = y2(t)
theta1 = theta1(t)
theta2 = theta2(t)

#define the system of equations of position
xc = xc
x1 = xc + l1*sin(theta1)
x2 = x1 + l2*sin(theta2)
y1 = - l1*cos(theta1)
y2 = y1 - l2*cos(theta2)

# Derivatives
dxc = d(xc,t)
dx1 = d(x1,t)
dx2 = d(x2,t)
dy1 = d(y1,t)
dy2 = d(y2,t)
ddxc = d(dxc,t)
ddx1 = d(dx1,t)
ddx2 = d(dx2,t)
ddy1 = d(dy1,t)
ddy2 = d(dy2,t)
dtheta1 = d(theta1,t)
dtheta2 = d(theta2,t)
ddtheta1 = d(dtheta1,t)
ddtheta2 = d(dtheta2,t)

F = M*ddxc


#kenetic energy

Tc = 1/2*M*(dxc**2)
T1 = 1/2*m1*(dx1**2 + dy1**2)
T2 = 1/2*m2*(dx2**2 + dy2**2)
T = Tc + T1 + T2

#potential energy
Vc = 0
V1 = m1*g*y1
V2 = m2*g*y2
V = Vc + V1 + V2

#Lagrangian
L = T - V


#Lagrange equation for xc
D_dxc = d(L,dxc)
D_dxc_dt = d(D_dxc,t)
D_xc = d(L,xc)

eq1 = D_dxc_dt - D_xc -F 

#Lagrange equation for theta1
D_dtheta1 = d(L,dtheta1)
D_dtheta1_dt = d(D_dtheta1,t)
D_dtheta1 = d(L,theta1)

eq2 = D_dtheta1_dt - D_dtheta1 

#Lagrange equation for theta2
D_dtheta2 = d(L,dtheta2)
D_dtheta2_dt = d(D_dtheta2,t)
D_dtheta2 = d(L,theta2)

eq3 = D_dtheta2_dt - D_dtheta2 


#equations of motion
eq1 = sp.simplify(eq1)
eq2 = sp.simplify(eq2)
eq3 = sp.simplify(eq3)

#solve for ddxc, ddtheta1, ddtheta2
sol = sp.solve([eq1,eq2,eq3],[ddxc,ddtheta1,ddtheta2],simplify=False,rational=False)

#substitute values
dzcdt_f = sp.lambdify((g,m1,m2,mc,l1,l2,xc,dxc,theta1,dtheta1,theta2,dtheta2,F),sol[ddxc])
dz1dt_f = sp.lambdify((g,m1,m2,mc,l1,l2,xc,dxc,theta1,dtheta1,theta2,dtheta2,F),sol[ddtheta1])
dz2dt_f = sp.lambdify((g,m1,m2,mc,l1,l2,xc,dxc,theta1,dtheta1,theta2,dtheta2,F),sol[ddtheta2])
dxcdt_f = sp.lambdify(dxc,dxc)
dtheta1dt_f = sp.lambdify(dtheta1,dtheta1)
dtheta2dt_f = sp.lambdify(dtheta2,dtheta2)

def dSdt(S, t, g, mc, m1, m2, l1, l2):
    xc, zc, theta1, z1, theta2, z2 = S
    return[
        dxcdt_f(zc),
        dzcdt_f(g,m1,m2,mc,l1,l2,xc,zc,theta1,z1,theta2,z2,F),
        dtheta1dt_f(z1),
        dz1dt_f(g,m1,m2,mc,l1,l2,xc,zc,theta1,z1,theta2,z2,0),
        dtheta2dt_f(z2),
        dz2dt_f(g,m1,m2,mc,l1,l2,xc,zc,theta1,z1,theta2,z2,0)
    ]

#initial conditions
t = np.linspace(0,40,1001)
g = 9.81
mc = 1
m1 = .6
m2 = .3
l1 = .2
l2 = .2
ans = odeint(dSdt, y0=[1, -3, -1 ,5], t=t, args=(g, mc, m1, m2, l1, l2))

#plotting
plt.plot(ans.T[0],ans.T[2])

plt.show()