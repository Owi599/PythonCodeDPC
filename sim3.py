import numpy as np
import sympy as sp
from sympy import symbols as sym
from sympy import sin as sin
from sympy import cos as cos
from sympy import diff as d
from sympy import Matrix as mat
from sympy import Function
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Constants
yc = 0
g = 9.81


#define constant symbols
mC , m1 , m2 = sym('mC m1 m2')
l1 , l2 = sym('l1 l2')

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

# define the position equations
xc = xc
x1 = xc + l1*sin(theta1)
x2 = x1 + l2*sin(theta2)

yc = 0
y1 = yc - l1*cos(theta1)
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
theta1 = theta1(t)
theta2 = theta2(t)
dtheta1 = d(theta1,t)
dtheta2 = d(theta2,t)
ddtheta1 = d(dtheta1,t)
ddtheta2 = d(dtheta2,t)

print(dy2)


