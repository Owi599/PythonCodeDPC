import numpy as np
import control as ct
import matplotlib.pyplot as plt
from scipy.linalg import solve_continuous_are
import time
from com import UDP, TCP
import random

# define UDP server
ETH_IP = "10.0.8.40"
ETH_IP_PI = "10.0.8.55"
FIVEG_IP = "10.0.3.55"
FIVEG_IP_PI = "10.0.5.13"
UDP_PORT_RECV_SENSORS = 890
UDP_PORT_CTRL = 5000


# Parameter defintion
pi = np.pi
mc = 0.232
m1 = 0.127
L1 = 0.3
LC1 = 0.3
I1 = m1 * LC1**2
g = 9.81


# Intermediates
h1 = mc + m1
h2 = m1 * LC1
h3 = m1 * L1**2 + I1
h4 = m1 * LC1 * g


#Server and Clients defined as objects of class COM
UDP_SENSORS = UDP(ETH_IP, UDP_PORT_RECV_SENSORS)
UDP_CTRL = UDP(ETH_IP_PI, UDP_PORT_CTRL)


# Dynamics
M = np.array(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, h1, h2],
        [0, 0, h2, h3],
    ]
)
N = np.array(
    [
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 0],
        [0, h4, 0, 0],
    ]
)
F = np.array([[0], [0], [1], [0]])

# linearized System Matrices
A = np.linalg.solve(M, N)
B = np.linalg.solve(M, F)
C = np.array([1, 0, 0, 0])
D = 0

# #test controllability
 
# print(A,B)
# ctrbl= ct.ctrb(A,B)
# print(np.linalg.matrix_rank(ctrbl))

#LQR Matrices
Q = np.array(
    [
        [1500, 0, 0, 0],
        [0, 1500, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]
)
R = np.array([[10]])

P = solve_continuous_are(A, B, Q, R)
K = np.linalg.inv(R) @ B.T @ P

# # calculate time constant

A_cl = A - B @ K


#eigenvalues of A_cl
eigenvalues = np.linalg.eigvals(A_cl)

#  dominant eigenvalue (the one with the smallest real part magnitude)
dominant_eigenvalue = min(eigenvalues, key=lambda ev: abs(ev.real))

# Calculate the time constant
time_constant = 1 / abs(dominant_eigenvalue.real)

#print(f"Eigenvalues: {eigenvalues}")
#print(f"Dominant Eigenvalue: {dominant_eigenvalue}")
print(f"Time Constant: {time_constant}")


def lqr_contol(x):
    return np.clip(-K @ x, -45,45)


#Exuction loop
while True:
    try:
        x0 = []
        lst = UDP_SENSORS.Rec_Message().split(" ")
        for element in lst:
            x0.append(float(element))
        print(x0)
        u = lqr_contol(x0)
        time.sleep(0.05)
        UDP_CTRL.Send_Message("{:.3f}".format(u[0]))

    except KeyboardInterrupt:
        break
    except Exception as e:
        print("An error occurred:", str(e))
