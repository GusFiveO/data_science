import pandas as pd
import matplotlib.pyplot as plt


def standardize_df(df):
    return (df - df.mean()) / df.std()


# test_file_path = "../Test_knight.csv"
train_file_path = "../Train_knight.csv"

# test_knights_df = pd.read_csv(test_file_path)

train_knights_df = pd.read_csv(train_file_path)


standardized_train_df = train_knights_df.select_dtypes(include="number")
standardized_train_df = standardize_df(standardized_train_df)
standardized_train_df["knight"] = train_knights_df["knight"]

print(train_knights_df)
print(standardized_train_df)


sith_df = standardized_train_df[standardized_train_df["knight"] == "Sith"]
jedi_df = standardized_train_df[standardized_train_df["knight"] == "Jedi"]


sith_friendship_standardized = sith_df["Friendship"]
jedi_friendship_standardized = jedi_df["Friendship"]


sith_mass_standardized = sith_df["Mass"]
jedi_mass_standardized = jedi_df["Mass"]

plt.scatter(
    sith_friendship_standardized,
    sith_mass_standardized,
    color="red",
    alpha=0.5,
    label="Sith",
)

plt.scatter(
    jedi_friendship_standardized,
    jedi_mass_standardized,
    color="blue",
    alpha=0.5,
    label="Jedi",
)

plt.legend()
plt.ylabel("Mass")
plt.xlabel("Friendship")

plt.show()
