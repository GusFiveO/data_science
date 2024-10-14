import pandas as pd
import matplotlib.pyplot as plt

test_file_path = "../Test_knight.csv"
train_file_path = "../Train_knight.csv"

test_knights_df = pd.read_csv(test_file_path)
nb_features = len(test_knights_df.columns)

fig, axs = plt.subplots(6, 5, figsize=(12, 10), layout="constrained")
i = 0
for series_name, series in test_knights_df.items():
    row = i // 5
    col = i % 5
    axs[row, col].hist(series, bins=40, color="limegreen")
    axs[row, col].set_title(series_name)
    axs[row, col].legend(["Knight"])
    i += 1
plt.show()

train_knights_df = pd.read_csv(train_file_path)
nb_features = len(test_knights_df.columns)

fig, axs = plt.subplots(6, 5, figsize=(12, 10), layout="constrained")
sith_df = train_knights_df[train_knights_df["knight"] == "Sith"].drop(columns="knight")
jedi_df = train_knights_df[train_knights_df["knight"] == "Jedi"].drop(columns="knight")

i = 0
for series_name, series in sith_df.items():
    row = i // 5
    col = i % 5
    axs[row, col].hist(series, bins=40, color="red", alpha=0.5, label="Sith")
    axs[row, col].set_title(series_name)
    axs[row, col].legend()
    i += 1

i = 0
for series_name, series in jedi_df.items():
    row = i // 5
    col = i % 5
    axs[row, col].hist(series, bins=40, color="blue", alpha=0.5, label="Jedi")
    axs[row, col].set_title(series_name)
    axs[row, col].legend()
    i += 1


plt.show()
