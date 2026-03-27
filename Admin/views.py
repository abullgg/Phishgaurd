from django.shortcuts import render,redirect
from Website.models import Phishing
# Create your views here.
def login(request):
    if request.method == "POST":
        usid = request.POST['username']
        pswd = request.POST['password']
        if usid == 'admin' and pswd == 'admin':
            return redirect('adminhome')

    return render(request,'adminlogin.html')

def adminhome(request):
    phishing=Phishing.objects.all()
    return render(request,"adminhome.html",{"phishing":phishing})