
from django.shortcuts import render, redirect

# Create your views here.

def home(request): # home 화면
    if request.method == 'GET' :
        return render(request, 'home.html')