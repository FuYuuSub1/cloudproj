import pandas as pd
import os

pwd = os.path.abspath(os.getcwd())

record_path = os.path.join(pwd, 'detail-records')


for filename in os.listdir(record_path):
    f = os.path.join(record_path, filename)

    if os.path.isfile(f):
        df = pd.read_csv(f)
    print(f)

