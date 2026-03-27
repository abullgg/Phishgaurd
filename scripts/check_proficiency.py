import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from joblib import load

# Load dataset
dataset_path = "datasets/Phishing.csv"
try:
    df = pd.read_csv(dataset_path)
    df.dropna(inplace=True)
    X = df["URL"]
    y = df["Label"]
    
    # Split using same parameters we would use
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
    
    # Load previously trained model
    model_path = "ml_models/phishing_model.pkl"
    pipeline = load(model_path)
    
    # Predict and evaluate
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Model Proficiency Report:")
    print(f"=========================")
    print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")

except Exception as e:
    print(f"Error checking model proficiency: {e}")
