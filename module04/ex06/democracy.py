from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import f1_score, precision_score
from sklearn.preprocessing import StandardScaler

import pandas as pd
import sys


def save_list(filename, list):
    with open(filename, "w") as txt_file:
        for line in list:
            txt_file.write(line + "\n")


train_file_path = sys.argv[1]
test_file_path = sys.argv[2]

train_df = pd.read_csv(train_file_path)
test_df = pd.read_csv(test_file_path)


validation_df = train_df.sample(frac=0.2, random_state=42)
train_df = train_df.drop(validation_df.index)

truth = validation_df["knight"]
validation_df = validation_df.drop("knight", axis=1)

target = train_df["knight"]
train_df = train_df.drop("knight", axis=1)

scaler = StandardScaler()
scaled_values = scaler.fit_transform(train_df)
train_df.loc[:, :] = scaled_values

scaled_values = scaler.fit_transform(validation_df)
validation_df.loc[:, :] = scaled_values

scaled_values = scaler.fit_transform(test_df)
test_df.loc[:, :] = scaled_values

knn = KNeighborsClassifier(n_neighbors=10)
rf = RandomForestClassifier()
lr = LogisticRegression()

votting_classifier = VotingClassifier(
    estimators=[("knn", knn), ("rf", rf), ("lr", lr)], voting="hard"
)

votting_classifier.fit(train_df, target)
prediction = votting_classifier.predict(validation_df)
print(
    "F1-Score:",
    f1_score(truth, prediction, labels=["Jedi", "Sith"], average="weighted"),
)
