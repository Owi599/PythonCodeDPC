import numpy as np
import control as ct
import matplotlib.pyplot as plt
from scipy.linalg import solve_continuous_are
import time
from udp import UDP

# define UDP server
UDP_IP = "10.0.3.40"
UDP_PI = "10.0.3.55"
UDP_PORT_RECV_ALPHA = 890
UDP_PORT_RECV_BETA = 892
UDP_PORT_RECV_X = 893
UDP_PORT_SEND = 5000

# Parameter defintion
pi = np.pi
mc = 0.232
m1 = 0.127
m2 = 0.127
L1 = 0.3
L2 = 0.3
LC1 = 0.3
LC2 = 0.3
I1 = m1 * LC1**2
I2 = m2 * LC2**2
g = 9.81
Bc = 0.5
B1 = 0.001
B2 = 0.001

# Intermediates
h1 = mc + m1 + m2
h2 = m1 * LC1 + m2 * L1
h3 = m2 * LC2
h4 = m2 * LC1**2 + m2 * L1**2 + I1
h5 = m2 * LC2 * L1
h6 = m2 * LC2**2 + I2
h7 = m1 * LC1 * g + m2 * L1 * g
h8 = m2 * LC2 * g

udpA = UDP(UDP_IP, UDP_PORT_RECV_ALPHA)
udpB = UDP(UDP_IP, UDP_PORT_RECV_BETA)
udpX = UDP(UDP_IP, UDP_PORT_RECV_X)


Alpha = udpA.Rec_Message()[0]
Beta = udpB.Rec_Message()[0]
x = udpX.Rec_Message()[0]

udpSend = UDP(UDP_PI,UDP_PORT_SEND)

x0 = np.array([[Alpha], [Beta], [x], [0], [0], [0]])

# Dynamics
M = np.array(
    [
        [1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, h1, h2, h3],
        [0, 0, 0, h2, h4, h5],
        [0, 0, 0, h3, h5, h6],
    ]
)
N = np.array(
    [
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0],
        [0, -h7, 0, 0, 0, 0],
        [0, 0, -h8, 0, 0, 0],
    ]
)
F = np.array([[0], [0], [0], [1], [0], [0]])

A = np.linalg.solve(M, N)
B = np.linalg.solve(M, F)
C = np.array([1, 0, 0, 0, 0, 0])
D = 0

Q = np.array(
    [
        [3000, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
    ]
)
R = np.array([[100]])

P = solve_continuous_are(A, B, Q, R)
K = np.linalg.inv(R) @ B.T @ P


def lqr_contol(x):
    return np.clip(-K @ x, -5, 5)


u = lqr_contol(x0)

print(u[0][0])

udpSend.Send_Message(float(u[0][0]))

