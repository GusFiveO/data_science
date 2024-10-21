from statsmodels.stats.outliers_influence import variance_inflation_factor
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler


def VIF(df):
    vif_data = pd.DataFrame()
    vif_data["feature"] = df.columns
    vif_data["VIF"] = [
        variance_inflation_factor(df.values, i) for i in range(len(df.columns))
    ]
    vif_data["Tolerance"] = 1 / vif_data["VIF"]
    print(vif_data)


train_file_path = "../Train_knight.csv"

train_df = pd.read_csv(train_file_path)

train_df = train_df.select_dtypes("number")

scaler = StandardScaler()
scaled_values = scaler.fit_transform(train_df)
train_df.loc[:, :] = scaled_values

VIF(train_df)

train_df = train_df.drop(
    [
        "Sensitivity",
        "Strength",
        "Recovery",
        "Stims",
        "Midi-chlorien",
        "Awareness",
        "Slash",
        "Empowered",
        "Delay",
        "Power",
        "Lightsaber",
        "Prescience",
        "Evade",
        "Attunement",
        "Dexterity",
        "Combo",
        "Repulse",
        "Burst",
    ],
    axis=1,
)
print("-----AFTER FEATURE SELECTION-----")
VIF(train_df)
corr = train_df.corr()

sns.heatmap(corr)
plt.show()
