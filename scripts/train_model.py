import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from nltk.tokenize import RegexpTokenizer
from joblib import dump
import os
import nltk

# Download 'punkt' if not already downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Load dataset
dataset_path = "datasets/Phishing.csv"  # Adjust if needed
df = pd.read_csv(dataset_path)

# Clean the data
df.dropna(inplace=True)
X = df["URL"]
y = df["Label"]

# Train-test split (optional, just for dev check)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build the redesigned ML pipeline using TF-IDF and n-grams
pipeline = make_pipeline(
    TfidfVectorizer(tokenizer=RegexpTokenizer(r'[A-Za-z]+').tokenize, stop_words="english", ngram_range=(1, 2)),
    LogisticRegression(max_iter=5000)
)

# Fit the model
pipeline.fit(X, y)

# Save the model to the models directory
os.makedirs("ml_models", exist_ok=True)
dump(pipeline, "ml_models/phishing_model.pkl")

print("Model trained and saved to 'ml_models/phishing_model.pkl'")
