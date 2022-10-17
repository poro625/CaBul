from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import authenticate, login as loginsession
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import get_user_model


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
        if password != password2:
            return render(request, 'signup.html')
        else:
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'signup.html')
            else:
                User.objects.create_user(username=username, password=password, email=email, nickname=nickname)
                return redirect('users:login') # 회원가입이 완료되었으므로 로그인 페이지로 이동


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



@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = User.objects.all().exclude(username=request.user.username)
        return render(request, 'follow.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user
    click_user = User.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('users:user-list')      