import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


train_file_path = "../Train_knight.csv"

train_df = pd.read_csv(train_file_path)

train_df = train_df.select_dtypes("number")
scaler = StandardScaler()
scaled_df = scaler.fit_transform(train_df)

var_ratio = []
for num in range(1, len(train_df.columns) + 1):
    pca = PCA(n_components=num)
    pca.fit(scaled_df)
    var_ratio.append(sum(pca.explained_variance_ratio_) * 100)

var_ratio = np.array(var_ratio)
print(pca.explained_variance_)
print(var_ratio)
plt.plot(var_ratio)
plt.show()
