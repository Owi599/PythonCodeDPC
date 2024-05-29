import numpy as np
import control as ct
import matplotlib.pyplot as plt
from scipy.linalg import solve_continuous_are
import time
from com import COM
import random

# define UDP server
ETH_IP = "10.0.8.40"
ETH_IP_PI = "10.0.8.55"
FIVEG_IP = "10.0.3.55"
FIVEG_IP_PI = "10.0.5.13"
UDP_PORT_RECV_ALPHA = 890
UDP_PORT_RECV_BETA = 892
UDP_PORT_RECV_X = 893
UDP_PORT_SEND = 5000
UDP = 1

# Parameter defintion
pi = np.pi
mc = 0.232
m1 = 0.127
L1 = 0.3
LC1 = 0.3
I1 = m1 * LC1**2
g = 9.81
Bc = 0.5
B1 = 0.001

# Intermediates
h1 = mc + m1 
h2 = m1 * LC1 
h3 =  m1 * L1**2 + I1
h4 = m1 * LC1 * g

udpA = COM(ETH_IP, UDP_PORT_RECV_ALPHA,UDP)
# udpB = COM(ETH_IP, UDP_PORT_RECV_BETA,UDP)
# udpX = COM(ETH_IP, UDP_PORT_RECV_X,UDP)



    
# Beta = udpB.Rec_Message()
# x = udpX.Rec_Message()

udpSend = COM(ETH_IP_PI,UDP_PORT_SEND,UDP)


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
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0],
        [0, -h4,0, 0],
    ]
)
F = np.array([ [0], [0], [1], [0]])

A = np.linalg.solve(M, N)
B = np.linalg.solve(M, F)
C = np.array([1, 0, 0, 0])
D = 0

Q = np.array(
    [
        [1000, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]
)
R = np.array([[20]])

P = solve_continuous_are(A, B, Q, R)
K = np.linalg.inv(R) @ B.T @ P


def lqr_contol(x):
    return np.clip(-K @ x, - 50,50)

while True:
    try:
        Alpha = float(udpA.Rec_Message())
        X = random.uniform(-0.5,0.5)
        # if Alpha < 0:
        #         Alpha = Alpha + 2*np.pi
        
        x0 = np.array([[X], [Alpha], [0], [0]])  
        time.sleep(0.001) 
        u = lqr_contol(x0)
        print(u[0][0],'',)
        udpSend.Send_Message(float(u[0][0]))
        
    except KeyboardInterrupt:
        break
    except Exception as e:
        print("An error occurred:", str(e))
    
