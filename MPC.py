import numpy as np
import sys
from casadi import *

# Add do_mpc to path. This is not necessary if it was installed via pip
import os
rel_do_mpc_path = os.path.join('..','..','..')
sys.path.append(rel_do_mpc_path)

import do_mpc

model_type = "continuous"  # either 'discrete' or 'continuous'
model = do_mpc.model.Model(model_type)

# Define the parameters
mc = 0.232
m1 = 0.1
m2 = 0.1
L1 = 0.3
L2 = 0.3

g = 9.81

# Define the derived parameters
LC1 = L1 / 2
LC2 = L2 / 2
I1 = (m1 * LC1**2) / 3
I2 = (m2 * LC2**2) / 3

# Define the intermediates
h1 = mc + m1 + m2
h2 = m1 * LC1 + m2 * L1
h3 = m2 * LC2
h4 = m1 * LC1**2 + m2 * L1**2 + I1
h5 = m2 * LC2 * L1
h6 = m2 * LC2**2 + I2
h7 = m1 * LC1 * g + m2 * L1 * g
h8 = m2 * LC2 * g

# Define the state variables
pos = model.set_variable("_x", "pos")
theta = model.set_variable("_x", "theta", shape=(2, 1))
dpos = model.set_variable("_x", "dpos")
dtheta = model.set_variable("_x", "dtheta", shape=(2, 1))

u = model.set_variable("_u", "force")

# Define the DAE

ddpos = model.set_variable("_z", "ddpos")
ddtheta = model.set_variable("_z", "ddtheta", shape=(2, 1))

# Define the ODE
model.set_rhs("pos", dpos)
model.set_rhs("theta", dtheta)
model.set_rhs("dpos", ddpos)
model.set_rhs("dtheta", ddtheta)

# Implement the Relation between the states and the algebraic variables
euler_lagrange = vertcat(
    # 1
    h1 * ddpos
    + h2 * ddtheta[0] * cos(theta[0])
    + h3 * ddtheta[1] * cos(theta[1])
    - (h2 * dtheta[0] ** 2 * sin(theta[0]) + h3 * dtheta[1] ** 2 * sin(theta[1]) + u),
    # 2
    h2 * cos(theta[0]) * ddpos
    + h4 * ddtheta[0]
    + h5 * cos(theta[0] - theta[1]) * ddtheta[1]
    - (h7 * sin(theta[0]) - h5 * dtheta[1] ** 2 * sin(theta[0] - theta[1])),
    # 3
    h3 * cos(theta[1]) * ddpos
    + h5 * cos(theta[0] - theta[1]) * ddtheta[0]
    + h6 * ddtheta[1]
    - (h5 * dtheta[0] ** 2 * sin(theta[0] - theta[1]) + h8 * sin(theta[1])),
)

model.set_alg("euler_lagrange", euler_lagrange)

# Define the Energie Euqations
E_kin_cart = 1 / 2 * mc * dpos**2
E_kin_p1 = (
    1
    / 2
    * m1
    * (
        (dpos + LC1 * dtheta[0] * cos(theta[0])) ** 2
        + (LC1 * dtheta[0] * sin(theta[0])) ** 2
    )
    + 1 / 2 * I1 * dtheta[0] ** 2
)
E_kin_p2 = (
    1
    / 2
    * m2
    * (
        (dpos + L1 * dtheta[0] * cos(theta[0]) + LC2 * dtheta[1] * cos(theta[1])) ** 2
        + (L1 * dtheta[0] * sin(theta[0]) + LC2 * dtheta[1] * sin(theta[1])) ** 2
    )
    + 1 / 2 * I2 * dtheta[0] ** 2
)

E_kin = E_kin_cart + E_kin_p1 + E_kin_p2

E_pot = m1 * g * LC1 * cos(theta[0]) + m2 * g * (
    L1 * cos(theta[0]) + LC2 * cos(theta[1])
)

model.set_expression("E_kin", E_kin)
model.set_expression("E_pot", E_pot)

model.setup()  # model build

# Define the controller
mpc = do_mpc.controller.MPC(model)

setup_mpc = {
    "n_horizon": 100,
    "n_robust": 0,
    "open_loop": 0,
    "t_step": 0.04,
    "state_discretization": "collocation",
    "collocation_type": "radau",
    "collocation_deg": 3,
    "collocation_ni": 1,
    "store_full_solution": True,
    # Use MA27 linear solver in ipopt for faster calculations:
    "nlpsol_opts": {"ipopt.linear_solver": "mumps"},
}
mpc.set_param(**setup_mpc)

mterm = model.aux["E_kin"] - model.aux["E_pot"]  # terminal cost
lterm = model.aux["E_kin"] - model.aux["E_pot"]  # stage cost

mpc.set_objective(mterm=mterm, lterm=lterm)
# Input force is implicitly restricted through the objective.
mpc.set_rterm(force=0.1)

mpc.bounds["lower", "_u", "force"] = -4
mpc.bounds["upper", "_u", "force"] = 4

mpc.setup()

# set up the estimator
estimator = do_mpc.estimator.StateFeedback(model)

simulator = do_mpc.simulator.Simulator(model)
params_simulator = {
    # Note: cvode doesn't support DAE systems.
    "integration_tool": "idas",
    "abstol": 1e-8,
    "reltol": 1e-8,
    "t_step": 0.04,
}

simulator.set_param(**params_simulator)
simulator.setup()

simulator.x0["theta"] = 0.99 * np.pi

x0 = simulator.x0.cat.full()

mpc.x0 = x0
estimator.x0 = x0

mpc.set_initial_guess()

import matplotlib.pyplot as plt

plt.ion()
from matplotlib import rcParams

rcParams["text.usetex"] = False
rcParams["axes.grid"] = True
rcParams["lines.linewidth"] = 2.0
rcParams["axes.labelsize"] = "xx-large"
rcParams["xtick.labelsize"] = "xx-large"
rcParams["ytick.labelsize"] = "xx-large"

mpc_graphics = do_mpc.graphics.Graphics(mpc.data)


def pendulum_bars(x):
    x = x.flatten()
    # Get the x,y coordinates of the two bars for the given state x.
    line_1_x = np.array([x[0], x[0] + L1 * np.sin(x[1])])

    line_1_y = np.array([0, L1 * np.cos(x[1])])

    line_2_x = np.array([line_1_x[1], line_1_x[1] + L2 * np.sin(x[2])])

    line_2_y = np.array([line_1_y[1], line_1_y[1] + L2 * np.cos(x[2])])

    line_1 = np.stack((line_1_x, line_1_y))
    line_2 = np.stack((line_2_x, line_2_y))

    return line_1, line_2


# capture

fig = plt.figure(figsize=(16, 9))

ax1 = plt.subplot2grid((4, 2), (0, 0), rowspan=4)
ax2 = plt.subplot2grid((4, 2), (0, 1))
ax3 = plt.subplot2grid((4, 2), (1, 1))
ax4 = plt.subplot2grid((4, 2), (2, 1))
ax5 = plt.subplot2grid((4, 2), (3, 1))

ax2.set_ylabel("$E_{kin}$ [J]")
ax3.set_ylabel("$E_{pot}$ [J]")
ax4.set_ylabel("Angle  [rad]")
ax5.set_ylabel("Input force [N]")

# Axis on the right.
for ax in [ax2, ax3, ax4, ax5]:
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()
    if ax != ax5:
        ax.xaxis.set_ticklabels([])

ax5.set_xlabel("time [s]")

mpc_graphics.add_line(var_type="_aux", var_name="E_kin", axis=ax2)
mpc_graphics.add_line(var_type="_aux", var_name="E_pot", axis=ax3)
mpc_graphics.add_line(var_type="_x", var_name="theta", axis=ax4)
mpc_graphics.add_line(var_type="_u", var_name="force", axis=ax5)

ax1.axhline(0, color="black")

bar1 = ax1.plot([], [], "-o", linewidth=5, markersize=10)
bar2 = ax1.plot([], [], "-o", linewidth=5, markersize=10)

ax1.set_xlim(-1.8, 1.8)
ax1.set_ylim(-1.2, 1.2)
ax1.set_axis_off()

fig.align_ylabels()
fig.tight_layout()

u0 = mpc.make_step(x0)
