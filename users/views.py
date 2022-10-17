from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import authenticate, login as loginsession
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.contrib.auth.hashers import check_password
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
            return render(request, 'signup.html', {'error': '패스워드를 확인 해 주세요!'})
        else:
            if email == '' or password == '':
                return render(request, 'signup.html', {'error': '이메일과 패스워드를 입력해주세요.'})
            
            exist_email = get_user_model().objects.filter(email=email)
            exist_nickname = get_user_model().objects.filter(nickname=nickname)
            if exist_email:
                return render(request, 'signup.html', {'error': '이미 존재하는 이메일입니다.'})
            elif exist_nickname:
                return render(request, 'signup.html', {'error': '이미 존재하는 닉네임입니다.'})
            else:
                User.objects.create_user(email=email, username=username, password=password, nickname=nickname)
                return render(request, 'login.html') # 회원가입이 완료되었으므로 로그인 페이지로 이동
        # if password == password2:
        #     User.objects.create_user(email=email, username=username, nickname=nickname, password=password)
        #     return render(request, 'login.html')
        # else:
        #     return HttpResponse("비밀번호가 틀렸습니다.")


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
    return render(request, 'signup.html')

def update(request, id):
    if request.method == 'GET':# 프로필 수정 페이지 접근
        return render(request, 'profile_edit.html')
    elif request.method =='POST':
        user = User.objects.get(id=id)
        user.username = request.POST.get('username')
        user.nickname = request.POST.get('nickname')
        
        exist_nickname = get_user_model().objects.filter(nickname=user.nickname)
        if exist_nickname:
            return render(request, 'profile_edit.html', {'error': '이미 존재하는 닉네임입니다.'})
        else:
            user.save()
        return redirect("/")

def password(request, id): # 비밀번호 변경 페이지 접근
    if request.method == 'GET':# 프로필 수정 페이지 접근
        return render(request, 'profile_edit_password.html')
    elif request.method == 'POST':
        user = User.objects.get(id=id)
        origin_password = request.POST["origin_password"]
        check = check_password(origin_password, user.password)
        if check:
            new_password = request.POST["new_password"]
            confirm_password = request.POST["confirm_password"]
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('/')
            else:
                return render(request, 'profile_edit_password.html', {'error':'새 비밀번호를 확인해주세요.'})
        else:
            return render(request, 'profile_edit_password.html', {'error':'비밀번호가 일치하지 않습니다'})
        