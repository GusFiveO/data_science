import pandas as pd
import sys

# train_file_path = "../Train_knight.csv"
try:
    train_file_path = sys.argv[1]

    train_knights_df = pd.read_csv(train_file_path)

    shuffled_df = train_knights_df.sample(frac=1)

    split_index = round(0.80 * len(shuffled_df))

    train_df = shuffled_df.iloc[:split_index, :]
    validation_df = shuffled_df.iloc[split_index:, :]

    train_df.to_csv("Training_knight.csv")
    validation_df.to_csv("Validation_knight.csv")
except Exception as e:
    print(e)
