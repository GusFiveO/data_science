import pandas as pd

train_file_path = "../Train_knight.csv"

train_df = pd.read_csv(train_file_path)

train_df = train_df.select_dtypes("number")

std_list = []
for series_name, serie in train_df.items():
    print(serie)
    std_list.append(float(serie.std()))
    # std_list.append(float(serie.var()))
print(std_list)
