import joblib
from .url_expander import expand_url

# Load the model globally ONCE when this module is imported. 
# This prevents disk I/O bottlenecks during requests.
try:
    ML_MODEL = joblib.load("ml_models/phishing_model.pkl")
except Exception as e:
    print(f"Warning: Failed to load ML model: {e}")
    ML_MODEL = None

def evaluate_url(original_url):
    """
    Expands the URL and evaluates it against the globally loaded ML model.
    Returns a dictionary with result details.
    """
    if ML_MODEL is None:
        raise RuntimeError("ML model is not loaded. Ensure ml_models/phishing_model.pkl exists.")

    final_url = expand_url(original_url)
    
    # Predict probabilities: [p_bad, p_good]
    proba = ML_MODEL.predict_proba([final_url])[0]
    p_bad, p_good = float(proba[0]), float(proba[1])
    
    THRESHOLD = 0.55
    is_phishing = p_bad >= THRESHOLD
    
    return {
        'original_url': original_url,
        'final_url': final_url,
        'p_bad': p_bad,
        'p_good': p_good,
        'is_phishing': is_phishing,
        'result_text': 'Phishing' if is_phishing else 'Safe'
    }
