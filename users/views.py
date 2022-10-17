from django.shortcuts import render
from .models import User
from django.contrib.auth import authenticate, login as loginsession
from django.http import HttpResponse


# Create your views here.
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password == password2:
            User.objects.create_user(email=email, username=username, nickname=nickname, password=password)
            return render(request, 'login.html')
        else:
            return HttpResponse("비밀번호가 틀렸습니다.")


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email , password=password)
        if user is not None:
            loginsession(request, user)

            return HttpResponse("로그인 성공")

        else:
            return HttpResponse("로그인 실패")