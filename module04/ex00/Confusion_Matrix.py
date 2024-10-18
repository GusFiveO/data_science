import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def load_file(file_path):
    with open(file_path) as file:
        return [line.strip() for line in file.readlines()]


def create_confusion_matrix(truth_list, predictions_list, mapping):
    matrix = np.zeros((2, 2), dtype=int)
    for truth, prediction in zip(truth_list, predictions_list):
        matrix[mapping[truth], mapping[prediction]] += 1
    return matrix


def calculate_scores(confusion_matrix):
    TP_jedi = confusion_matrix[0, 0]
    FP_jedi = confusion_matrix[0, 1]
    FN_jedi = confusion_matrix[1, 0]
    TN_jedi = confusion_matrix[1, 1]

    precision_jedi = TP_jedi / (TP_jedi + FP_jedi)
    recall_jedi = TP_jedi / (TP_jedi + FN_jedi)
    f1_jedi = 2 * (precision_jedi * recall_jedi) / (precision_jedi + recall_jedi)

    precision_sith = TN_jedi / (TN_jedi + FN_jedi)
    recall_sith = TN_jedi / (TN_jedi + FP_jedi)
    f1_sith = 2 * (precision_sith * recall_sith) / (precision_sith + recall_sith)

    accuracy = (TP_jedi + TN_jedi) / np.sum(confusion_matrix)

    total_jedi = TP_jedi + FN_jedi
    total_sith = TN_jedi + FP_jedi

    return {
        "precision_jedi": precision_jedi,
        "recall_jedi": recall_jedi,
        "f1_jedi": f1_jedi,
        "precision_sith": precision_sith,
        "recall_sith": recall_sith,
        "f1_sith": f1_sith,
        "accuracy": accuracy,
        "total_jedi": total_jedi,
        "total_sith": total_sith,
    }


def print_scores(scores):
    print(f"{'Class':<10} {'Precision':<10} {'Recall':<10} {'F1-Score':<10} {'Total'}")
    print(
        f"{'Jedi':<10} {scores['precision_jedi']:.2f}      {scores['recall_jedi']:.2f}          {scores['f1_jedi']:.2f}       {scores['total_jedi']}"
    )
    print(
        f"{'Sith':<10} {scores['precision_sith']:.2f}      {scores['recall_sith']:.2f}          {scores['f1_sith']:.2f}       {scores['total_sith']}"
    )
    print(
        f"{'Accuracy':<10}                         {scores['accuracy']:.2f}      {scores['total_jedi'] + scores['total_sith']}"
    )


def plot_confusion_matrix(confusion_matrix, labels):
    sns.heatmap(
        confusion_matrix,
        annot=True,
        vmin=0,
        cmap="flare",
        xticklabels=labels,
        yticklabels=labels,
    )
    plt.ylabel("Truth")
    plt.xlabel("Prediction")
    plt.title("Confusion Matrix")
    plt.show()


truth_file_path = "../truth.txt"
predictions_file_path = "../predictions.txt"

truth_list = load_file(truth_file_path)
predictions_list = load_file(predictions_file_path)

mapping = {"Jedi": 0, "Sith": 1}
labels = ["Jedi", "Sith"]

conf_matrix = create_confusion_matrix(truth_list, predictions_list, mapping)

scores = calculate_scores(conf_matrix)

print_scores(scores)

plot_confusion_matrix(conf_matrix, labels)
