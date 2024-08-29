import numpy as np  # library for nummeric operations
import control as ct # control library 
import matplotlib.pyplot as plt # visualization library 
from scipy.linalg import solve_continuous_are # linearization library 
import time # time library
from com import UDP, TCP # importing self made class

#  UDP server parameters
ETH_IP = "10.0.8.40"
ETH_IP_PI = "10.0.8.55"
FIVEG_IP = "10.0.3.55"
FIVEG_IP_PI = "10.0.5.13"
UDP_PORT_RECV_SENSORS = 890
UDP_PORT_CTRL = 5000


# Parameter defintion for pendel
pi = np.pi
mc = 0.232 # cart mass
m1 = 0.127 # mass of pendulum arm 1
m2 = 0.127 # mass of pendulum arm 2
L1 = 0.3   # length of first arm 
L2 = 0.3   # length of second arm
LC1 = 0.3
LC2 = 0.3
I1 = m1 * LC1**2 # moment of inertia 1
I2 = m2 * LC2**2 # moment of inertia 2
g = 9.81


# Intermediates
h1 = mc + m1 + m2
h2 = m1 * LC1 + m2 * L1
h3 = m2 * LC2
h4 = m2 * LC1**2 + m2 * L1**2 + I1
h5 = m2 * LC2 * L1
h6 = m2 * LC2**2 + I2
h7 = m1 * LC1 * g + m2 * L1 * g
h8 = m2 * LC2 * g

#Server and Clients defined as objects of class COM
UDP_SENSORS = UDP(ETH_IP, UDP_PORT_RECV_SENSORS)
UDP_CTRL = UDP(ETH_IP_PI, UDP_PORT_CTRL)


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

# linearized System Matrices
A = np.linalg.solve(M, N)
B = np.linalg.solve(M, F)
C = np.array([1, 0, 0, 0, 0, 0])
D = 0

#LQR Matrices
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
R = np.array([[10]])

P = solve_continuous_are(A, B, Q, R)
K = np.linalg.inv(R) @ B.T @ P


def lqr_contol(x):
    return np.clip(-K @ x, -20, 20)

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
    
