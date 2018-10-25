#!/usr/bin/python3

import numpy as np

coeficients = np.array([[1,1,-1],[1,0,0]])
constants = np.array([0,0])
matrix = np.array([[1,1,-1,0],[1,0,0,0]])


# NO solution - different rank of coeficients and augmented matrix
# same ranks, there exists at least one solution
# rank < #of unknowns - infinit solutions

print(np.column_stack((coeficients,constants)))
print(np.linalg.matrix_rank(matrix))
print(np.linalg.solve(matrix,constants))