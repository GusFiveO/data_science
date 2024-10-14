import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

test_file_path = "../Test_knight.csv"
train_file_path = "../Train_knight.csv"

test_knights_df = pd.read_csv(test_file_path)
train_knights_df = pd.read_csv(train_file_path)

sith_df = train_knights_df[train_knights_df["knight"] == "Sith"].drop(columns="knight")
jedi_df = train_knights_df[train_knights_df["knight"] == "Jedi"].drop(columns="knight")

train_knights_df.replace({"Sith": 0, "Jedi": 1}, inplace=True)

fig, axs = plt.subplots(2, 2, figsize=(4, 4))


axs[0, 0].scatter(
    sith_df["Friendship"], sith_df["Mass"], color="red", alpha=0.5, label="Sith"
)
axs[0, 0].scatter(
    jedi_df["Friendship"], jedi_df["Mass"], color="blue", alpha=0.5, label="Jedi"
)

axs[0, 0].set_ylabel("Mass")
axs[0, 0].set_xlabel("Friendship")

axs[0, 0].legend()

axs[1, 0].scatter(
    test_knights_df["Friendship"],
    test_knights_df["Mass"],
    color="green",
    alpha=0.5,
    label="Knight",
)

axs[1, 0].set_ylabel("Mass")
axs[1, 0].set_xlabel("Friendship")

axs[1, 0].legend()

axs[0, 1].scatter(
    sith_df["Sensitivity"], sith_df["Empowered"], color="red", alpha=0.5, label="Sith"
)
axs[0, 1].scatter(
    jedi_df["Sensitivity"], jedi_df["Empowered"], color="blue", alpha=0.5, label="Jedi"
)
axs[0, 1].legend()

axs[0, 1].set_ylabel("Empowered")
axs[0, 1].set_xlabel("Sensitivity")

axs[1, 1].scatter(
    test_knights_df["Sensitivity"],
    test_knights_df["Empowered"],
    color="green",
    alpha=0.5,
    label="Knight",
)

axs[1, 1].legend()

axs[1, 1].set_ylabel("Empowered")
axs[1, 1].set_xlabel("Sensitivity")
plt.show()
