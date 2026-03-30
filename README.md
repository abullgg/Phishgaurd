# PhishGuard 

PhishGuard is a full-stack **Machine Learning** application built with Django that detects and prevents zero-day phishing links using lexical URL analysis. 

![Dependencies](https://img.shields.io/badge/dependencies-Django%20|%20scikit--learn-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

##  Features

- **Lexical ML Evaluation:** Bypasses traditional blocklists by analyzing the URL syntax dynamically via a Custom `TfidfVectorizer` and `LogisticRegression` pipeline. Evaluates probabilities against a strict `0.55` threshold for accurate zero-day detection.
- **High-Performance Inference Engine:** The ML pipeline (`phishing_model.pkl`) is loaded globally upon server initialization via `services/ml_engine.py`, guaranteeing instant, zero-latency inference without disk I/O bottlenecks. 
- **Glassmorphism UI:** Built with premium Tailwind CSS styling to ensure a polished user experience.
- **Advanced Admin Tracking Dashboard:** Caches and reports predicted URLs, storing precise `confidence_score` metrics and timestamped (`added_on`) audit trails in an internal portal for active monitoring.
- **RESTful API Endpoint:** Interact with the phishing prediction engine programmatically by parsing JSON requests through `/api/predict`.

---

##  Stack

- **Backend:** Python, Django 4.x
- **Frontend:** HTML5, Tailwind CSS, FontAwesome
- **Data Science / ML:** Scikit-Learn, Pandas, NLTK, Joblib

---

##  Installation & Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YourUsername/PhishGuard.git
   cd PhishGuard
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start the local server:**
   ```bash
   python manage.py runserver
   ```
   *Navigate to `http://127.0.0.1:8000/` in your browser.*

---

## ☁️ Deployment (Render)

This project is fully configured for a seamless deployment to [Render](https://render.com). It utilizes `gunicorn` for serving the WSGI application and `whitenoise` for serving static Tailwind CSS files.

1. Set up a new **Web Service** on Render connected to this repository.
2. Under "Build Command", enter:
   ```bash
   sh build.sh
   ```
3. Under "Start Command", enter:
   ```bash
   gunicorn Phishing.wsgi
   ```
4. Click **Deploy**!

---

##  API Documentation

You can hit the backend evaluation logic without using the UI.
**Endpoint:** `POST /api/predict`

**Payload Content-Type:** `application/x-www-form-urlencoded` or `application/json`

**Example Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/predict/ \
     -d "url=http://secure-update-paypal.com/login"
```

**JSON Response:**
```json
{
  "url": "http://secure-update-paypal.com/login",
  "result": "Phishing",
  "confidence_score": 0.893
}
```

---

##  Retraining the Model

To ensure you have the latest metrics, you can retrain the `.pkl` artifact from scratch against the provided datasets.
```bash
python scripts/train_model.py
```
This script will construct a TF-IDF vector matrix over `datasets/Phishing.csv` and dump the resulting pipeline directly into `ml_models/`.
