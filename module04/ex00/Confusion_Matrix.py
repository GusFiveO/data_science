import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

truth_file_path = "../truth.txt"
predictions_file_path = "../predictions.txt"


def load_file(file_path):
    with open(file_path) as truth_file:
        line = truth_file.readline()
        res = []
        while len(line):
            res.append(line.strip())
            line = truth_file.readline()
    return res


truth_list = load_file(truth_file_path)
predictions_list = load_file(predictions_file_path)

mapping = {"Jedi": 1, "Sith": 0}
labels = ["Jedi", "Sith"]


truth_list = [mapping[elem] for elem in truth_list]
predictions_list = [mapping[elem] for elem in predictions_list]


confusion_matrix = np.matrix("0 0; 0 0")

for truth, prediction in zip(truth_list, predictions_list):
    confusion_matrix[1 - truth, 1 - prediction] += 1
    # confusion_matrix[truth, prediction] += 1

TP_jedi = confusion_matrix[0, 0]
FP_jedi = confusion_matrix[0, 1]
FN_jedi = confusion_matrix[1, 0]
TN_jedi = confusion_matrix[1, 1]

TP_sith = TN_jedi
FP_sith = FN_jedi
FN_sith = FP_jedi
TN_sith = TP_jedi

# Calculating Precision
precision_jedi = TP_jedi / (TP_jedi + FP_jedi)
precision_sith = TP_sith / (TP_sith + FP_sith)

# Calculating Recall
recall_jedi = TP_jedi / (TP_jedi + FN_jedi)
recall_sith = TP_sith / (TP_sith + FN_sith)

# Calculating F1-Score
f1_jedi = 2 * (precision_jedi * recall_jedi) / (precision_jedi + recall_jedi)
f1_sith = 2 * (precision_sith * recall_sith) / (precision_sith + recall_sith)

# Calculating Accuracy
accuracy = (TP_jedi + TN_jedi) / (TP_jedi + FP_jedi + FN_jedi + TN_jedi)

# Total Support (number of actual instances per class)
total_jedi = TP_jedi + FN_jedi
total_sith = TP_sith + FN_sith

# Printing the results
print(f"{'Class':<10} {'Precision':<10} {'Recall':<10} {'F1-Score':<10} {'Total'}")
print(
    f"{'Jedi':<10} {precision_jedi:.2f}      {recall_jedi:.2f}          {f1_jedi:.2f}       {total_jedi}"
)
print(
    f"{'Sith':<10} {precision_sith:.2f}      {recall_sith:.2f}          {f1_sith:.2f}       {total_sith}"
)
print(
    f"{'Accuracy':<10}                         {accuracy:.2f}      {total_jedi + total_sith}"
)

print(confusion_matrix)
sns.color_palette("flare", as_cmap=True)
sns.heatmap(confusion_matrix, annot=True, vmin=0, cmap="flare")
plt.ylabel("Truth")
plt.xlabel("Prediction")
plt.title("Confusion Matrix")
plt.show()
