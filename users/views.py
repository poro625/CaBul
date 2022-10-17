from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import authenticate, login as loginsession
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth

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
            return redirect('/')
        else:
            return HttpResponse("로그인 실패")

@login_required
def logout(request):   #로그아웃 함수
    auth.logout(request) # 인증 되어있는 정보를 없애기
    return redirect("/")

@login_required
def delete(request):   #회원탈퇴
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('users/signup')

def update(request, id):
    if request.method == 'GET':# 프로필 수정 페이지 접근
        return render(request, 'profile_edit.html')
    elif request.method =='POST':
        user = User.objects.get(id=id)
        user.username = request.POST.get('username')
        user.nickname = request.POST.get('nickname')
        user.save()
        return redirect("/")

def password(request, id): # 비밀번호 변경 페이지 접근
    if request.method == 'GET':# 프로필 수정 페이지 접근
        return render(request, 'profile_edit_password.html')
