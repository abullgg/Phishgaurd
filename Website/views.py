import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Phishing
from services.ml_engine import evaluate_url

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
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(first_name=firstName, last_name=lastName, email=email, username=username, password=password)
                user.save()
                messages.success(request, 'Account created successfully! Please sign in.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')

        return redirect('register')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('data')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return render(request, "index.html")

def detailed_analysis(request):
    if 'result' not in request.session:
        return redirect('data')

    return render(request, 'detailed_analysis.html', {
        'url': request.session['last_final_url'],
        'result': request.session['result'],
        'p_bad': request.session['p_bad'],
        'p_good': request.session['p_good'],
    })

def predict(request):
    if request.method == "POST":
        original_url = request.POST['url']
        
        try:
            # Reusable ML logic from ml_engine
            eval_result = evaluate_url(original_url)
            
            # store session
            request.session['last_original_url'] = eval_result['original_url']
            request.session['last_final_url'] = eval_result['final_url']
            request.session['p_bad'] = eval_result['p_bad']
            request.session['p_good'] = eval_result['p_good']
            request.session['result'] = 'bad' if eval_result['is_phishing'] else 'good'

            # Update database with result and the new fields
            Phishing.objects.create(
                url=eval_result['original_url'], 
                output=eval_result['result_text'],
                confidence_score=eval_result['p_bad']
            )
            
        except RuntimeError as e:
            messages.error(request, str(e))
            return render(request, 'data.html')

        return redirect('analysis')

    return render(request, 'data.html')

@csrf_exempt
def api_predict(request):
    if request.method == "POST":
        original_url = request.POST.get('url') or ""
        
        # In case the payload is json
        if not original_url:
            try:
                data = json.loads(request.body)
                original_url = data.get('url', "")
            except:
                pass

        if not original_url:
            return JsonResponse({'error': 'No URL provided'}, status=400)

        try:
            # Reusable ML logic
            eval_result = evaluate_url(original_url)
            
            # Store query with detailed fields for Admin View
            Phishing.objects.create(
                url=eval_result['original_url'], 
                output=eval_result['result_text'],
                confidence_score=eval_result['p_bad']
            )

            return JsonResponse({
                'url': eval_result['original_url'],
                'result': eval_result['result_text'],
                'confidence_score': eval_result['p_bad']
            })
        except RuntimeError as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)
