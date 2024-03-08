import numpy as np
import control as ct
import matplotlib.pyplot as plt
from scipy.linalg import solve_continuous_are
import socket

# define UDP server
UDP_IP = "192.168.2.106"
UDP_PORT_RECV_ALPHA = 890
UDP_PORT_RECV_BETA = 892
UDP_PORT_RECV_X = 893
UDP_PORT_SEND = 891
sock_recv_a = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_recv_b = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_recv_x = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def UDP_Angle_Alpha():
    while True:
        sock_recv_a.bind((UDP_IP, UDP_PORT_RECV_ALPHA))
        data, addr = sock_recv_a.recvfrom(1024)  # buffer size is 1024 bytes
        return data.decode()


def UDP_Angle_Beta():
    while True:
        sock_recv_b.bind((UDP_IP, UDP_PORT_RECV_BETA))
        data, addr = sock_recv_b.recvfrom(1024)  # buffer size is 1024 bytes
        return data.decode()


def UDP_Cart_Position():
    while True:
        sock_recv_x.bind((UDP_IP, UDP_PORT_RECV_X))
        data, addr = sock_recv_x.recvfrom(1024)  # buffer size is 1024 bytes
        return data.decode()


def UDP_send_data(data):
    sock_send.sendto(data.encode(), (UDP_IP, UDP_PORT_SEND))


A = UDP_Angle_Alpha()
B = UDP_Angle_Beta()
C = UDP_Cart_Position()

# convert strings to float values and split
A = float(A)
B = float(B)
C = float(C)


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

x0 = np.array([[C], [A], [B], [0.0], [0.0], [0.0]])  # initial state Vector

# Intermediates
h1 = mc + m1 + m2
h2 = m1 * LC1 + m2 * L1
h3 = m2 * LC2
h4 = m2 * LC1**2 + m2 * L1**2 + I1
h5 = m2 * LC2 * L1
h6 = m2 * LC2**2 + I2
h7 = m1 * LC1 * g + m2 * L1 * g
h8 = m2 * LC2 * g

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
Ctrl = ct.ctrb(A, B)
Rank = np.linalg.matrix_rank(Ctrl)

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
    while True:
        return np.clip(-K @ x, -5, 5)


u = lqr_contol(x0)
print(u)

# K, S, E = ct.lqr(A, B, Q, R)
# BK = B @ K
# sys = ct.ss((A - BK), B, C, D)

# t = np.arange(0, 30, 0.005)
# t, y, x = ct.initial_response(sys, T=t, X0=x0, return_x=True)

# # Plot results
# plt.figure()
# plt.xlabel("t in s")
# plt.ylabel("x in m / theta in rad")
# plt.plot(t, x[1], "b--", label="theta_1")
# plt.plot(t, x[2], "r:", label="theta_2")
# plt.plot(t, x[0], "g", label="x")
# plt.legend(loc="best")
# plt.grid(True)

# plt.figure()
# plt.xlabel("t in s")
# plt.ylabel("x_dot in m/s / theta_dot in rad/s")
# plt.plot(t, x[4], "b--", label="theta_1_dot")
# plt.plot(t, x[5], "r:", label="theta_2_dot")
# plt.plot(t, x[3], "g", label="x_dot")
# plt.legend(loc="best")
# plt.grid(True)
# plt.show()
