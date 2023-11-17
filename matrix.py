import numpy as np
import sympy as sp
from sympy import symbols as sym
from sympy import Matrix as mat

# Constants
alpha1 = sym('alpha1')
alpha2 = sym('alpha2')

# define constant symbols
A = mat([[1, 0, 0],[0, 1, alpha1],[0, alpha2, 1]])

inversed = A.inv()

print(inversed)
 