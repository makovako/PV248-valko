#!/usr/bin/python3

import csv, sys, json
import pandas as pd
import numpy as np


df = pd.read_csv(sys.argv[1])
id = sys.argv[2]

output = {}

if id == "average":
    pass
else:
    # print(df.to_string())
    dates = set()
    exercises = set()
    headers = df.columns.values[1:]
    for header in headers:         
        dates.add(header.split("/")[0].strip())
        exercises.add(header.split("/")[1].strip())
    exercises = list(exercises)
    exercises.sort()
    dates = list(dates)
    dates.sort()
    ls = df.index[df['student']==int(id)].tolist()
    id = ls[0]
    expoints = {}
    datepoints = {}
    for ex in exercises:
        expoints[ex] = 0
    for date in dates:
        datepoints[date] = 0
    for ex in exercises:
        for header in headers:
            if "/"+ex in header:
                if df.at[id,header] > expoints[ex]:
                    expoints[ex] = df.at[id,header]
    for i in range(len(dates)):
        for header in headers:
            date = dates[i]
            if date in header:
                if i > 0:
                    datepoints[date] = df.at[id,header] + datepoints[date]
                else:
                    datepoints[date] = df.at[id,header]
    for i in range(1,len(dates)):
        datepoints[dates[i]] += datepoints[dates[i-1]]
    print(expoints) 
    print(datepoints)
    output["mean"] = np.mean(list(expoints.values()))
    output["median"] = np.median(list(expoints.values()))
    output["passed"] = np.count_nonzero(list(expoints.values()))
    output["total"] = np.sum(list(expoints.values()))

print(json.dumps(output,indent=4,ensure_ascii=False))
