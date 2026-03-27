from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Phishing
import joblib

def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')

        if password == c_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
            else:
                user = User.objects.create_user(first_name=firstName, last_name=lastName, email=email, username=username, password=password)
                user.save()
                return render(request, 'login.html')
        else:
            messages.info(request, 'Passwords do not match')

        return render(request, 'register.html')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user:
            return render(request, 'data.html')
        else:
            messages.info(request, 'Invalid credentials')
            return render(request, 'login.html')
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return render(request, "index.html")

from .models import Phishing

def detailed_analysis(request):
    if 'result' not in request.session:
        return redirect('data')

    return render(request, 'detailed_analysis.html', {
    'url': request.session['last_final_url'],
    'result': request.session['result'],
    'p_bad': request.session['p_bad'],
    'p_good': request.session['p_good'],
})





from services.url_expander import expand_url
import joblib

def predict(request):
    if request.method == "POST":
        original_url = request.POST['url']
        final_url = expand_url(original_url)

        model = joblib.load("ml_models/phishing_model.pkl")
        proba = model.predict_proba([final_url])[0]
        p_bad, p_good = proba

        THRESHOLD = 0.75
        is_phishing = p_bad >= THRESHOLD

        # store session
        request.session['last_original_url'] = original_url
        request.session['last_final_url'] = final_url
        request.session['p_bad'] = float(p_bad)
        request.session['p_good'] = float(p_good)
        request.session['result'] = 'bad' if is_phishing else 'good'

        # Update database with result
        Phishing.objects.create(url=original_url, output="Phishing" if is_phishing else "Safe")

        return redirect('analysis')

    return render(request, 'data.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def api_predict(request):
    if request.method == "POST":
        original_url = request.POST.get('url') or ""
        
        # In case the payload is json
        if not original_url:
            import json
            try:
                data = json.loads(request.body)
                original_url = data.get('url', "")
            except:
                pass

        if not original_url:
            return JsonResponse({'error': 'No URL provided'}, status=400)

        final_url = expand_url(original_url)

        model = joblib.load("ml_models/phishing_model.pkl")
        proba = model.predict_proba([final_url])[0]
        p_bad, p_good = proba

        THRESHOLD = 0.75
        is_phishing = p_bad >= THRESHOLD
        
        # Store query
        Phishing.objects.create(url=original_url, output="Phishing" if is_phishing else "Safe")

        return JsonResponse({
            'url': original_url,
            'result': 'Phishing' if is_phishing else 'Safe',
            'confidence_score': float(p_bad)
        })
    return JsonResponse({'error': 'Method not allowed'}, status=405)
