📱 Samsung Mobile Reviews – Sentiment Analysis
Using Digikala API | Persian Text Processing | Machine Learning


⭐ About the Project

This repository contains a complete end-to-end sentiment analysis pipeline on Persian user reviews of Samsung mobile phones, collected directly from the Digikala API.

The project includes:

✔ Automated data collection from Digikala API (products + comments)
✔ Full data cleaning & preprocessing for Persian text
✔ TF-IDF vectorization optimized for short Persian reviews
✔ Handling imbalanced classes using targeted oversampling
✔ Training multiple ML models (Naive Bayes, Logistic Regression, Linear SVM)
✔ Evaluation using Accuracy, Precision, Recall, F1-score, and Confusion Matrix


📂 Repository Structure

├── fetch_data.py                # Script to collect raw data from Digikala API
├── samsung_mobiles.csv          # Final cleaned dataset used for modeling
├── sentiment_analysis.ipynb     # Main notebook: preprocessing → training → evaluation
└── README.md                    # Project documentation


📊 Dataset Overview

The dataset contains user reviews for Samsung mobile phones:
| Column                                               | Description                             |
| ---------------------------------------------------- | --------------------------------------- |
| `body`                                               | Original user comment                   |
| `sentiment`                                          | Label assigned based on Digikala rating |
| `comment`                                            | Preprocessed Persian text               |
| `label`                                              | Encoded label                           |
| (+ extracted product features from API in raw files) |                                         |


🧠 Sentiment Classes

Reviews were categorized into:
- Positive
- Neutral
- Negative

Based on the numeric rating provided by users on Digikala.


🛠 Machine Learning Models Used

We trained and compared:
- Naive Bayes (Best Performance)
- Logistic Regression
- Linear SVM

Best model selected based on weighted F1-score and overall metrics.


📈 Evaluation Metrics

All models were evaluated using:
- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix

Final results (example):
| Model               | Accuracy | F1-score |
| ------------------- | -------- | -------- |
| **Naive Bayes**     | **0.78** | **0.71** |
| Logistic Regression | 0.69     | 0.70     |
| Linear SVM          | 0.73     | 0.71     |


🚀 How to Run the Project
1. Install dependencies:
    pip install -r requirements.txt
2. Run data collection (optional):
    python fetch_data.py
3. Open the notebook:
    jupyter notebook sentiment_analysis.ipynb


⚙ Preprocessing Techniques

- Persian text normalization
- Removing non-Persian characters
- Tokenization
- Stopword removal
- No stemming (better performance for short reviews)
- TF-IDF with n-grams (1,2)