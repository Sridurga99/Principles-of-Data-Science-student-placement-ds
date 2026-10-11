# PlacementIQ – Student Placement Intelligence

## Student Placement Prediction and Skill Gap Analysis Using Data Science

PlacementIQ is an end-to-end Data Science and Machine Learning project that analyzes student placement data to predict placement readiness, identify placement-related factors, analyze student skill gaps, segment students, and provide personalized recommendations through an interactive Streamlit dashboard.

## Objectives

- Predict student placement status
- Identify factors associated with placement
- Compare multiple machine learning models
- Explain model predictions
- Segment students using clustering
- Identify student skill gaps
- Generate personalized recommendations
- Provide an interactive placement analytics dashboard

## Features

### Dataset Explorer
- Dataset filtering
- Student record search
- Feature distribution analysis
- Placement status filtering
- CSV download

### EDA & Insights
- Placement rate analysis
- Branch-wise placement analysis
- Correlation analysis
- Placed vs non-placed student comparison
- Academic and skill-based analysis

### Placement Prediction
Predicts placement status using:

- CGPA
- Coding skills
- Aptitude score
- Communication skills
- Internships
- Certifications
- Projects
- Backlogs
- Degree
- Branch
- Gender
- Age

### Model Explanation
Uses Logistic Regression coefficients to understand the features influencing the model's placement prediction.

### Student Segmentation
Uses K-Means clustering based on:

- CGPA
- Coding skills
- Aptitude score
- Backlogs
- Internships
- Projects

### Skill Gap Analysis
Compares a student's current profile with placed-student benchmarks and identifies areas that require improvement.

### Model Comparison

| Model | Test Accuracy |
|---|---:|
| Logistic Regression | 85.67% |
| Decision Tree | 100.00% |
| Random Forest | 100.00% |
| XGBoost | 100.00% |

Logistic Regression was selected as the deployed model because of its interpretability, while all four models are retained for comparison.

### Recommendations
Provides personalized placement-readiness recommendations based on identified skill gaps.

## Dataset

The cleaned dataset contains:

- 12,000 students
- 13 columns
- 3,652 placed students
- 8,348 non-placed students
- 30.43% placement rate
- 0 missing values
- 0 duplicate rows

### Dataset Features

- gender
- age
- degree
- branch
- cgpa
- backlogs
- internships
- certifications
- coding_skills
- communication_skills
- aptitude_score
- projects
- placed

## Machine Learning Workflow

Raw Dataset  
↓  
Data Cleaning  
↓  
Train/Test Split  
↓  
Categorical Encoding  
↓  
Feature Scaling  
↓  
Model Training  
↓  
Model Evaluation  
↓  
Model Selection  
↓  
Placement Prediction  
↓  
Model Explanation  
↓  
Student Segmentation  
↓  
Skill Gap Analysis  
↓  
Personalized Recommendations  
↓  
Streamlit Dashboard

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- Matplotlib
- Seaborn
- Plotly
- Streamlit
- Joblib
- Jupyter Notebook
- Google Colab

## Project Structure

student-placement-ds/

├── app/  
│   ├── app.py  
│   ├── theme.py  
│   ├── home.py  
│   ├── dataset_explorer.py  
│   ├── eda.py  
│   ├── prediction.py  
│   ├── explanation.py  
│   ├── segmentation.py  
│   ├── skill_gap.py  
│   ├── model_comparison.py  
│   └── recommendations.py  
│  
├── data/  
│   ├── raw/  
│   └── processed/  
│       └── student_placement_cleaned.csv  
│  
├── models/  
│   ├── best_model.pkl  
│   ├── encoder.pkl  
│   ├── scaler.pkl  
│   ├── kmeans_model.pkl  
│   ├── cluster_scaler.pkl  
│   ├── cluster_profiles.csv  
│   ├── cluster_placement.csv  
│   └── model_comparison.csv  
│  
├── notebooks/  
│   ├── 03_eda.ipynb  
│   ├── 04_placement_prediction.ipynb  
│   ├── 05_model_explanation.ipynb  
│   ├── 06_student_segmentation.ipynb  
│   └── 07_skill_gap_analysis.ipynb  
│  
├── visualizations/  
├── create_cleaned_dataset.py  
├── inspect_dataset.py  
├── requirements.txt  
└── README.md

## Installation

### Clone the Repository

git clone https://github.com/Sridurga99/Principles-of-Data-Science-student-placement-ds.git

### Navigate to the Project

cd Principles-of-Data-Science-student-placement-ds

### Create Virtual Environment

python -m venv .venv

### Activate Virtual Environment

.venv\Scripts\activate

### Install Dependencies

pip install -r requirements.txt

## Run the Application

python -m streamlit run app/app.py

The application will open at:

http://localhost:8501

## Dashboard Pages

1. Overview
2. Dataset Explorer
3. EDA & Insights
4. Placement Prediction
5. Model Explanation
6. Student Segmentation
7. Skill Gap Analysis
8. Model Comparison
9. Recommendations

## Important Findings

The strongest correlations with placement in the dataset are:

| Feature | Correlation |
|---|---:|
| Coding Skills | 0.463 |
| Aptitude Score | 0.390 |
| CGPA | 0.265 |
| Internships | 0.017 |
| Certifications | 0.007 |
| Backlogs | -0.001 |
| Communication Skills | -0.006 |
| Age | -0.007 |
| Projects | -0.023 |

These values represent patterns in the dataset and do not imply causation.

## Model Limitations

- The dataset may not represent all real-world student populations.
- Perfect accuracy from some models may indicate dataset-specific separation.
- Prediction probabilities are estimates.
- Correlation does not imply causation.
- Predictions should not be considered actual hiring decisions.
- Recommendations do not guarantee placement.

## Future Enhancements

- Company-specific placement prediction
- Salary prediction
- External dataset validation
- Model monitoring
- Data drift detection
- Online deployment
- Student authentication
- Personalized student accounts

## Author

Sri Durga R

B.Tech Artificial Intelligence & Data Science  
Rajalakshmi Engineering College

## GitHub Repository

https://github.com/Sridurga99/Principles-of-Data-Science-student-placement-ds

## Disclaimer

This project is developed for academic and educational purposes. Placement predictions and recommendations are intended to support student analysis and development and should not be considered a guarantee of employment.