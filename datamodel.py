import pandas as pd
import numpy as np

df = pd.read_csv("fetchalldf.csv")

#remove id, names
df = df.drop(columns=["id", "name"])



print(df)