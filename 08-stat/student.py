#!/usr/bin/python3

import csv, sys, json
import pandas as pd
import numpy as np
from datetime import date as dt
from datetime import timedelta as td
from scipy import stats

def dateToTuple(date):
    a,b,c = date.strip().split("-")
    return int(a),int(b),int(c)

df = pd.read_csv(sys.argv[1])
id = sys.argv[2]

output = {}

if id == "average":
    df = pd.DataFrame(df.mean().to_dict(),index=[0])
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
    ls = df.index[df['student']==0].tolist()
    # print(ls)
    id = 0
    expoints = {}
    datepoints = {}
    for ex in exercises:
        expoints[ex] = 0
    for date in dates:
        datepoints[date] = 0
    for ex in exercises:
        for header in headers:
            if "/"+ex in header:
                expoints[ex] += df.at[id,header]
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
    # print(expoints) 
    # print(datepoints)
    output["mean"] = np.mean(list(expoints.values()))
    output["median"] = np.median(list(expoints.values()))
    output["passed"] = int(np.count_nonzero(list(expoints.values())))
    output["total"] = float(np.sum(list(expoints.values())))
    start = "2018-09-17"
    x = []
    x.append(0)
    for date in dates:
        delta = (dt(*dateToTuple(date))- dt(*dateToTuple(start))).days
        x.append(delta)
    y = []
    y.append(0)
    y.extend(datepoints.values())
    # print(x)
    # print(y)

    x = np.array(x)
    y = np.array(y)
    # x = np.vstack([x, np.ones(len(x))]).T
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    sl , _ ,_ ,_ = np.linalg.lstsq(x.reshape(-1,1),y,rcond=None)
 
    matrix = np.stack([x**d for d in [1]], axis=-1)

    slo, incpt, _, _ = np.linalg.lstsq(matrix,y,rcond=None) # toto pouzi

    if float(slo) != 0:
        output["regression slope"] = float(slo)
        end16 = dt(*dateToTuple(start)) + td(days=int(16/slo))
        end20 = dt(*dateToTuple(start)) + td(days=int(20/slo))

        output["date 16"] = end16.strftime("%Y-%m-%d")
        output["date 20"] = end20.strftime("%Y-%m-%d")
    else:
        output["regression slope"] = float(slo)


else:
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
    output["mean"] = float(np.mean(list(expoints.values())))
    output["median"] = float(np.median(list(expoints.values())))
    output["passed"] = int(np.count_nonzero(list(expoints.values())))
    output["total"] = float(np.sum(list(expoints.values())))
    start = "2018-09-17"
    x = []
    x.append(0)
    for date in dates:
        delta = (dt(*dateToTuple(date))- dt(*dateToTuple(start))).days
        x.append(delta)
    y = []
    y.append(0)
    y.extend(datepoints.values())

    x = np.array(x)
    y = np.array(y)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    sl , inc ,_ ,_ = np.linalg.lstsq(x.reshape(-1,1),y,rcond=None)

    # TODO slope = 0 - nevypisuj slope 16 a 20

    matrix = np.stack([x**d for d in [1]], axis=-1)
    slo, incpt, _, _ = np.linalg.lstsq(matrix,y,rcond=None) # toto pouzi

    if float(slo) != 0.0:
        output["regression slope"] = float(slo)
        end16 = dt(*dateToTuple(start)) + td(days=int(16/slo))
        end20 = dt(*dateToTuple(start)) + td(days=int(20/slo))

        output["date 16"] = end16.strftime("%Y-%m-%d")
        output["date 20"] = end20.strftime("%Y-%m-%d")
    else:
        output["regression slope"] = float(slo)

print(json.dumps(output,indent=4,ensure_ascii=False))
