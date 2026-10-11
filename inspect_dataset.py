import pandas as pd

file_path = "data/raw/archive (7)/Indian_Student_Placement_Dataset_2025.csv"

df = pd.read_csv(file_path)

print("\nDATASET SHAPE:")
print(df.shape)

print("\nCOLUMN NAMES:")
print(df.columns.tolist())

print("\nFIRST 5 ROWS:")
print(df.head())

print("\nDATA TYPES:")
print(df.dtypes)