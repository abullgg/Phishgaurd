import joblib
import pandas as pd

# URLs gathered from PhishTank reports and current phishing samples
test_urls = [
    "http://secure-update-paypal.com/login",
    "https://amazon-security-verification-alert.net/auth",
    "http://support-appleid.apple.com.authorize-device.net/",
    "http://banco-security-chile.info/login.php",
    "https://login-microsoftonline-com.web-app.io/"
]

def check_phishtank_urls():
    print("Loading redesigned ML model...")
    model = joblib.load("ml_models/phishing_model.pkl")
    
    print("-" * 50)
    print("Testing against known PhishTank links:")
    print("-" * 50)
    
    for url in test_urls:
        proba = model.predict_proba([url])[0]
        p_bad, p_good = proba
        
        is_phishing = p_bad >= 0.75
        result = "PHISHING" if is_phishing else "SAFE"
        
        print(f"URL: {url}")
        print(f"Prediction: {result} (Risk score: {p_bad:.2%})")
        print("-" * 50)

if __name__ == "__main__":
    check_phishtank_urls()
