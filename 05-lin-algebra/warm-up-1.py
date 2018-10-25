#!/usr/bin/python3

import numpy as np

matrix = np.array([[4,7],[2,6]])

print(np.linalg.matrix_rank(matrix))
print(np.linalg.det(matrix))
print(np.linalg.inv(matrix))
# print(numpy.linalg.matrix_rank(numpy.array(matrix)))