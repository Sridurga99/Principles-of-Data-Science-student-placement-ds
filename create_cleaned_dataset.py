import pandas as pd
import os

input_file = "data/raw/archive (7)/Indian_Student_Placement_Dataset_2025.csv"
output_file = "data/processed/student_placement_cleaned.csv"

df = pd.read_csv(input_file)

# Keep the columns needed for analysis and machine learning
columns_to_keep = [
    "gender",
    "age",
    "degree",
    "branch",
    "cgpa",
    "backlogs",
    "internships",
    "certifications",
    "coding_skills",
    "communication_skills",
    "aptitude_score",
    "projects",
    "placed"
]

cleaned_df = df[columns_to_keep].copy()

os.makedirs("data/processed", exist_ok=True)

cleaned_df.to_csv(output_file, index=False)

print("CLEANED DATASET CREATED")
print("Shape:", cleaned_df.shape)
print("File:", output_file)
print("\nColumns:")
print(cleaned_df.columns.tolist())
print("\nMissing values:")
print(cleaned_df.isnull().sum())