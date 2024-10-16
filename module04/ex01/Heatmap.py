import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("future.no_silent_downcasting", True)

train_file_path = "../Train_knight.csv"

train_df = pd.read_csv(train_file_path)

train_df.replace({"Sith": 0, "Jedi": 1}, inplace=True)

corr = train_df.corr()

sns.heatmap(corr)
plt.show()
