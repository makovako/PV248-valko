#!/usr/bin/python3

import sys,re
import numpy as np

constants = [] # matrix of constants
coeficients = [] # matrix of int coeficients

lines = [] # list of dicts with variables and their coeficients e.g. [{"x":1,"y":1},{"y":2,"x":3}]
variables = set() # set of all used variables

for line in open(sys.argv[1],"r"):
    left, right = line.strip().split("=")
    constants.append(int(right.strip()))
    left.strip()    
    positive = True
    number = ""
    line_variables = {} # variables and their coeficients e. g. {"x":12,"y":3}
    for char in left:
        if char == "+":
            positive = True
        elif char == "-":
            positive = False
        elif ord(char) >= 97 and ord(char) <= 122: #its variable
            variables.add(char)
            if number == "":
                number = "1"
            if not positive:
                number = "-" + number
            
            line_variables[char] = int(number)
            number = ""
        elif ord(char) >= 48 and ord(char) <= 57:
            number += char
        else:
            continue
    lines.append(line_variables)

variables = list(variables)
variables.sort()

# create coeficients matrix
for line in lines:
    coeficient_line = []
    for var in variables: 
        if var in line:
            coeficient_line.append(line[var])
        else:
            coeficient_line.append(0)
    coeficients.append(coeficient_line)

augmented_matrix = np.column_stack((coeficients,constants))
coeficients_rank = np.linalg.matrix_rank(coeficients)
augmented_rank = np.linalg.matrix_rank(augmented_matrix)
dimension = len(variables) - coeficients_rank

debug = False
if debug:
    print("Variables set sorted: {}".format(variables))
    print("Parsed equations: {}".format(lines))
    print("Coef_rank: {}, Aug_rank: {}".format(coeficients_rank,augmented_rank))

    print("Coeficients: {}".format(coeficients))
    print("Augmented matrix: {}".format(augmented_matrix))

if coeficients_rank != augmented_rank:
    print("no solution")
else:
    if coeficients_rank == len(variables):
        # print solution TODO
        answer = ""
        solution = np.linalg.solve(coeficients,constants)
        for i in range(len(variables)):
            answer += " {} = {},".format(variables[i],int(solution[i]) if solution[i].is_integer() else solution[i])
        print("solution:{}".format(answer[:-1]))
    else:
        print("solution space dimension: {}".format(dimension))



