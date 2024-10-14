import matplotlib.pyplot as plt
import pandas as pd

pd.set_option("future.no_silent_downcasting", True)

train_file_path = "../Train_knight.csv"

train_knights_df = pd.read_csv(train_file_path)
train_knights_df.replace({"Sith": 0, "Jedi": 1}, inplace=True)

corr = train_knights_df.corr()["knight"]
print(corr.sort_values(ascending=False))
