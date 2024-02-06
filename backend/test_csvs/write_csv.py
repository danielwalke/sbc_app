import random

import pandas as pd
from random import  randrange, uniform
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--rows", "--r", help="number of random rows", type=int)
args = parser.parse_args()
ROWS = args.rows
columns = "patient_id;age;sex;hgb;wbc;rbc;mcv;plt;groundTruth".split(";")
df = pd.DataFrame(columns = columns)
for i in range(ROWS):
	df.loc[len(df.index)] = [len(df.index),randrange(120),"W", uniform(0, 20),
uniform(0,1000), uniform(0, 50), uniform(0, 100), uniform(0,2000), random.randint(0, 1)]
df.to_csv("test.csv",index=False, sep = ";")
