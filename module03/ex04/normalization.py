import pandas as pd
import matplotlib.pyplot as plt


def normalize_df(df):
    return (df - df.min()) / (df.max() - df.min())


# test_file_path = "../Test_knight.csv"
train_file_path = "../Train_knight.csv"

# test_knights_df = pd.read_csv(test_file_path)

train_knights_df = pd.read_csv(train_file_path)

normalized_train_df = train_knights_df.select_dtypes(include="number")
normalized_train_df = normalize_df(normalized_train_df)
normalized_train_df["knight"] = train_knights_df["knight"]

print(train_knights_df)
print(normalized_train_df)

sith_df = normalized_train_df[normalized_train_df["knight"] == "Sith"]
jedi_df = normalized_train_df[normalized_train_df["knight"] == "Jedi"]

sith_sensitivity_normalized = sith_df["Sensitivity"]
jedi_sensitivity_normalized = jedi_df["Sensitivity"]

sith_empowered_normalized = sith_df["Empowered"]
jedi_empowered_normalized = jedi_df["Empowered"]

plt.scatter(
    sith_sensitivity_normalized,
    sith_empowered_normalized,
    color="red",
    alpha=0.5,
    label="Sith",
)

plt.scatter(
    jedi_sensitivity_normalized,
    jedi_empowered_normalized,
    color="blue",
    alpha=0.5,
    label="Jedi",
)

plt.legend()
plt.ylabel("Empowered")
plt.xlabel("Sensitivity")

plt.show()
