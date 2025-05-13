import numpy as np                                                      # library for nummeric operations
import control as ct                                                    # control library 
from scipy.linalg import solve_continuous_are, solve_discrete_are       # linearization library 
import time                                                             # time library
from com import UDP, TCP                                                # importing self made communication class
from lqr import LQR                                                     # importing self made controller class


#  UDP server parameters
ethClient = "10.0.8.40"
ethServer = "10.0.8.55"
fiveGClient = "10.0.3.55"
fiveGCLint = "10.0.5.13"
ethPortSensor = 890
ethPortControl = 5000


#Server and Clients defined as objects of class COM
UDPSENSORS = UDP(ethClient, ethPortSensor)
UDPCONTROL = UDP(ethServer, ethPortControl)
client = UDPSENSORS.create_client()
server = UDPSENSORS.create_server()
# Pendulum Parameters
pi = np.pi              # Constant for pi
m_c = 0.232              # Mass of the cart
m_1 = 0.127              # Mass of the first pendulum
m_2 = 0.127              # Mass of the second pendulum
l_1 = 0.3                # Length of the first pendulum
l_2 = 0.3                # Length of the second pendulum
lc_1 = 0.3               # Length to center of mass of the first pendulum
lc_2 = 0.15              # Length to center of mass of the second pendulum
i_1 = m_1 * lc_1**2        # Moment of inertia of the first pendulum
i_2 = m_2 * lc_2**2        # Moment of inertia of the second pendulum
g = 9.81                # Gravitational acceleration 

# i_ntermedi_ate calculati_ons for the system matrices
h_1 = m_c + m_1 + m_2
h_2 = m_1 * lc_1 + m_2 * l_1
h_3 = m_2 * lc_2
h_4 = m_2 * lc_1**2 + m_2 * l_1**2 + i_1
h_5 = m_2 * lc_2 * l_1
h_6 = m_2 * lc_2**2 + i_2
h_7 = m_1 * lc_1 * g + m_2 * l_1 * g
h_8 = m_2 * lc_2 * g

# System matrix representati_on
M = np.array([
    [1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0],
    [0, 0, 0, h_1, h_2, h_3],
    [0, 0, 0, h_2, h_4, h_5],
    [0, 0, 0, h_3, h_5, h_6],
])
N = np.array([
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0],
    [0, -h_7, 0, 0, 0, 0],
    [0, 0, -h_8, 0, 0, 0],
])
F = np.array([[0], [0], [0], [1], [0], [0]])

# linearized System Matrices
A = np.linalg.solve(M, N)
B = np.linalg.solve(M, F)
C = np.array([[1, 0, 0, 0, 0, 0]])
D = np.array([[0]])
t_s = 0.02  # Sampling time in seconds

#LQR Matrices
Q = np.diag([4000, 50, 50, 100, 10, 10])  # State cost matrix
R = np.array([[100]])

CONTROLLER = LQR(A, B, C, D, Q, R)
sys_C, sys_D = CONTROLLER.covert_continuous_to_discrete(A, B, C, D, t_s)

K_d = CONTROLLER.compute_K_discrete(Q, R, sys_D)


# #Exuction loop
try:
    while True:
        x_0 = []
        lst = UDPSENSORS.receive_data(server).split(" ")
        for element in lst:
            x_0.append(float(element))
        print('Received Sensor Data:',x_0) 
        u = CONTROLLER.compute_control_output_discrete(K_d, x_0)
        print('Computed Control Output:',u)
        UDPCONTROL.send_data("{:.3f}".format(u[0]),client)
        
except KeyboardInterrupt:
    print("Execution interrupted by user.")
except Exception as e:
    print("An error occurred:", str(e))
