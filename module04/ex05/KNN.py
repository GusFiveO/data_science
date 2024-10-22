import matplotlib.pyplot as plt
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import sys
from sklearn.metrics import f1_score, precision_score


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

    precision_list = []
    for k_value in range(1, 41):
        knn = KNeighborsClassifier(n_neighbors=k_value)
        knn.fit(train_df, target)
        prediction = knn.predict(validation_df)
        precision_list.append(
            precision_score(
                truth, prediction, labels=["Jedi", "Sith"], average="weighted"
            )
        )
    max_index = precision_list.index(max(precision_list))
    knn = KNeighborsClassifier(n_neighbors=40)
    knn.fit(train_df, target)
    prediction = knn.predict(validation_df)
    print(
        "F1-Score:",
        f1_score(truth, prediction, labels=["Jedi", "Sith"], average="weighted"),
    )
    test_predi = knn.predict(test_df)
    save_list("KNN.txt", test_predi)
    plt.plot(precision_list)
    plt.ylabel("precision")
    plt.xlabel("k values")
    plt.show()
except Exception as e:
    print(e)
