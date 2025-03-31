import numpy as np  # library for nummeric operations
import control as ct # control library 
import matplotlib.pyplot as plt # visualization library 
from scipy.linalg import solve_continuous_are, solve_discrete_are # linearization library 
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
mc = 0.232 # cart mass in Kg
m1 = 0.127 # mass of pendulum arm 1 in Kg
m2 = 0.127 # mass of pendulum arm 2 in Kg
L1 = 0.3   # length of first arm in m
L2 = 0.3   # length of second arm in m
LC1 = 0.3 # in m
LC2 = 0.15 # in m
I1 = m1 * LC1**2 # moment of inertia 1 in kg.m^2
I2 = m2 * LC2**2 # moment of inertia 2 in kg.m^2
g = 9.81 # in m/s^2


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
print(B)
C = np.array([[1, 0, 0, 0, 0, 0]])
D = np.array([[0]])
T_s = 0.3  # Sampling time in seconds

# Create StateSpace object
Sys_C = ct.StateSpace(A, B, C, D)
Sys_D = ct.c2d(Sys_C, T_s)  # Convert to discrete system
A_d, B_d, C_d, D_d = Sys_D.A, Sys_D.B, Sys_D.C, Sys_D.D  # Extract matrices

ctrbl= ct.ctrb(A,B)
print(np.linalg.matrix_rank(ctrbl))
#LQR Matrices
Q = np.array(
    [
        [4000, 0, 0, 0, 0, 0],
        [0, 50, 0, 0, 0, 0],
        [0, 0, 50, 0, 0, 0],
        [0, 0, 0, 100, 0, 0],
        [0, 0, 0, 0, 10, 0],
        [0, 0, 0, 0, 0, 10],
    ]
)
R = np.array([[100]])

P = solve_continuous_are(A, B, Q, R)
P_d = solve_discrete_are(A_d, B_d, Q, R)
K = np.linalg.inv(R) @ B.T @ P
K_d = np.linalg.inv(R + B_d.T @ P_d @ B_d) @ (B_d.T @ P_d @ A_d)
print(K)
A_cl = A - B @ K
A_cl_d = A_d - B_d @ K_d
# Compute the eigenvalues of A_cl
eigenvalues = np.linalg.eigvals(A_cl)
eigenvalues_d = np.linalg.eigvals(A_cl_d)

# Find the dominant eigenvalue (the one with the smallest real part magnitude)
dominant_eigenvalue = min(eigenvalues, key=lambda ev: abs(ev.real))
dominant_eigenvalue_d = min(eigenvalues_d, key=lambda ev: abs(ev.real))

# Calculate the time constant
time_constant = 1 / abs(dominant_eigenvalue.real)
time_constant_d = 1 / abs(dominant_eigenvalue_d.real)
print(f"Eigenvalues: {eigenvalues}")
print(f"Dominant Eigenvalue: {dominant_eigenvalue}")
print(f"Time Constant: {time_constant}")

print(f"Eigenvalues_d: {eigenvalues_d}")
print(f"Dominant Eigenvalue_d: {dominant_eigenvalue_d}")
print(f"Time Constant_d: {time_constant_d}")
def lqr_contol(x):
    return np.clip(-K @ x, -8.5, +8.5)

def lqr_contol_d(x_k):
    return np.clip(-K_d @ x_k, -8.5, +8.5)

# #Exuction loop
while True:
    try:
        x0 = []
        lst = UDP_SENSORS.Rec_Message().split(" ")
        for element in lst:
            x0.append(float(element))
        print(x0) 
        u = lqr_contol_d(x0)
        print(u)
        #time.sleep(0.1)
        UDP_CTRL.Send_Message("{:.3f}".format(u[0]))
        time.sleep(T_s/2)

    except KeyboardInterrupt:
        break
    except Exception as e:
        print("An error occurred:", str(e))
