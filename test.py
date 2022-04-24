import pandas as pd
import os

pwd = os.path.abspath(os.getcwd())

record_path = os.path.join(pwd, 'SparkAggregatedData')

for filename in os.listdir(record_path):
    f = os.path.join(record_path, filename)
    with open(f) as file:
        lines = file.readlines()
        for i in lines:
            i = i.replace("(","").replace(")","").replace(" ","").replace("'", "").replace("\n","")
            li = list(i.split(","))
            
    