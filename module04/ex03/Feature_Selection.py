from statsmodels.stats.outliers_influence import variance_inflation_factor
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler

train_file_path = "../Train_knight.csv"

train_df = pd.read_csv(train_file_path)

train_df = train_df.select_dtypes("number")

scaler = StandardScaler()
scaled_values = scaler.fit_transform(train_df)
train_df.loc[:, :] = scaled_values

vif_data = pd.DataFrame()
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
vif_data["feature"] = train_df.columns
vif_data["VIF"] = [
    variance_inflation_factor(train_df.values, i) for i in range(len(train_df.columns))
]
print(vif_data)
corr = train_df.corr()

sns.heatmap(corr)
plt.show()
