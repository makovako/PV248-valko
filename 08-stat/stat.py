#!/usr/bin/python3
import csv, sys
import pandas as pd

df = pd.read_csv("points.csv")

input_file = sys.argv[1]
mode = sys.argv[2]

# print(df.columns)

output = {}
if mode == "dates":
    dates = []
    for line in open(input_file,"r"):
        dates.append(line)
    for date in dates:
        headers = []
        for header in df.columns:         
            if date in header:
                headers.append(header)
        mean = df[headers].mean()
        print(mean)
        median = df[headers].median().median()
        last = df[headers]
        first = df[headers].quantile(0.75)
        print(median)
        print(last)
        print(first)
        
            
        
    
    pass    
if mode == "deadlines":
    pass
if mode == "exercises":
    pass


    