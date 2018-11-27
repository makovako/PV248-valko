#!/usr/bin/python3
import csv, sys, json
import pandas as pd

df = pd.read_csv(sys.argv[1])
mode = sys.argv[2]
output = {}
if mode == "dates":
    dates = set()
    headers = df.columns.values[1:]
    dateheader = {}
    for header in headers:         
        dates.add(header.split("/")[0].strip())
    dates = list(dates)
    dates.sort()
    for date in dates:
        dateheader[date] = []
    for date in dates:
        for header in headers:
            if date in header:
                dateheader[date].append(header)
    for k,v in dateheader.items():
        mean = 0
        out = {}
        for col in v:
            data = df[col]
            mean += data.mean()
        x = []
        for col in v:
            x.append(df[col])
        data = pd.concat(x)
        out["mean"] = mean
        out["median"] = data.median()
        out["passed"] = len(data[data > 0])
        out["first"] = data.quantile(0.25)
        out["last"] = data.quantile(0.75)
        output[k.strip()] = out
if mode == "deadlines":
    headers = df.columns.values[1:]
    for header in headers:
        out = {}
        out["mean"] = df[header].mean()
        out["median"] = df[header].median()
        out["passed"] = len(df[df[header]>0])
        out["first"] = df[header].quantile(0.25)
        out["last"] = df[header].quantile(0.75)
        output[header.strip()] = out
    
if mode == "exercises":
    exercises = set()
    headers = df.columns.values[1:]
    exheader = {}
    for header in headers:
        exercises.add(header.split("/")[1].strip())
    exercises = list(exercises)
    exercises.sort()
    for ex in exercises:
        exheader[ex] = []
    for ex in exercises:
        for header in headers:
            if "/"+ex in header:
                exheader[ex].append(header)
    for k,v in exheader.items():
        out = {}
        mean = 0
        for col in v:
            data = df[col]
            mean += data.mean()
        x = []
        for col in v:
            x.append(df[col])
        data = pd.concat(x)
        out["mean"] = mean
        out["median"] = data.median()
        out["passed"] = len(data[data > 0])
        out["first"] = data.quantile(0.25)
        out["last"] = data.quantile(0.75)
        output[k.strip()] = out
        

print(json.dumps(output,indent=4,ensure_ascii=False))
