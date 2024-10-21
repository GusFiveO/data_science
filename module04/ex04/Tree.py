import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from sklearn.preprocessing import StandardScaler

from sklearn import tree
import matplotlib.pyplot as plt

from sklearn.metrics import f1_score
import numpy as np

import sys


def load_file(file_path):
    with open(file_path) as file:
        return np.array([line.strip() for line in file.readlines()])


def save_list(filename, list):
    with open(filename, "w") as txt_file:
        for line in list:
            txt_file.write(line + "\n")


def feature_selection(df):
    return df.drop(
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


try:
    train_file_path = sys.argv[1]
    test_file_path = sys.argv[2]

    train_df = pd.read_csv(train_file_path)
    test_df = pd.read_csv(test_file_path)

    validation_df = train_df.sample(frac=0.2, random_state=42)
    train_df = train_df.drop(validation_df.index)

    truth = validation_df["knight"]
    target = train_df["knight"]
    train_df = train_df.drop("knight", axis=1)

    truth = validation_df["knight"]
    validation_df = validation_df.drop("knight", axis=1)

    validation_df = feature_selection(validation_df)
    train_df = feature_selection(train_df)
    test_df = feature_selection(test_df)

    scaler = StandardScaler()
    scaled_values = scaler.fit_transform(train_df)
    train_df.loc[:, :] = scaled_values

    scaled_values = scaler.fit_transform(validation_df)
    validation_df.loc[:, :] = scaled_values

    clf = RandomForestClassifier(class_weight="balanced")
    clf.fit(train_df, target)

    prediction = clf.predict(validation_df)
    print(
        "F1-Score:",
        f1_score(truth, prediction, labels=["Jedi", "Sith"], average="weighted"),
    )

    test_prediction = clf.predict(test_df)
    save_list("Tree.txt", test_prediction)

    fig, axes = plt.subplots(dpi=900)
    tree.plot_tree(
        clf.estimators_[0],
        feature_names=train_df.columns,
        class_names=["Jedi", "Sith"],
        filled=True,
    )

    plt.savefig("Tree")
except Exception as e:
    print(e)
