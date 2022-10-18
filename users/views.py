from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import authenticate, login as loginsession
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.http import JsonResponse

import re
import requests
import random
import string


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
        profile_image = 'default.png'

        if password != password2:
            return render(request, 'signup.html', {'error': '패스워드를 확인 해 주세요!'})
        elif (len(password) < 8 ):
            return render(request, 'signup.html', {'error': '패스워드는 8자 이상이어야 합니다!'})
        elif re.search('[a-zA-z]+', password)is None:
            return render(request, 'signup.html', {'error': '비밀번호는 최소 1개 이상의 영문이 포함되어야 합니다!'})
        elif re.search('[0-9]+', password) is None:
            return render(request, 'signup.html', {'error': '비밀번호에는 최소 1개 이상의 숫자가 포함되어야 합니다!'})
        elif re.search('[`~!@#$%^&*(),<.>/?]+', password) is None:
            return render(request, 'signup.html', {'error': '비밀번호에는 최소 1개 이상의 특수문자가 포함되어야 합니다!'})
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
                User.objects.create_user(email=email, username=username, password=password, nickname=nickname, profile_image=profile_image)
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
        return render(request, 'profile_edit.html')
    
def profileupload(request, id):
    if request.method == 'GET':
        return render(request, 'profileupload.html')
    elif request.method =='POST':
        user = User.objects.get(id=id)
        user.profile_image = request.FILES['image']
        
        user.save()
        return render(request, 'profileupload.html')

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


def kakao_social_login(request):
    if request.method == 'GET':
        client_id = '1d6d8f64503403d8949492c6632d2da3'
        redirect_uri = 'http://127.0.0.1:8000/account/login/kakao/callback'
        return redirect(
            f'https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code'
        )


def kakao_social_login_callback(request):
    try:
        code = request.GET.get('code')
        client_id = '1d6d8f64503403d8949492c6632d2da3'
        redirect_uri = 'http://127.0.0.1:8000/account/login/kakao/callback'
        token_request = requests.post(
            'https://kauth.kakao.com/oauth/token', {'grant_type': 'authorization_code',
                                                    'client_id': client_id, 'redierect_uri': redirect_uri, 'code': code}
        )
        # token_request = requests.get(
        # f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}'
        # )
        token_json = token_request.json()

        error = token_json.get('error', None)

        if error is not None:
            print(error)
            return JsonResponse({"message": "INVALID_CODE"}, status=400)

        access_token = token_json.get("access_token")

    except KeyError:
        return JsonResponse({"message": "INVALID_TOKEN"}, status=400)

    except access_token.DoesNotExist:
        return JsonResponse({"message": "INVALID_TOKEN"}, status=400)

        #------get kakaotalk profile info------#

    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    kakao_id = profile_json.get('id')
    username = profile_json['properties']['nickname']

    if User.objects.filter(kakao_id=kakao_id).exists():
        user = User.objects.get(kakao_id=kakao_id)
        auth.login(request, user)  # 로그인 처리
    else:
        User.objects.create(
            username=username,

            kakao_id=kakao_id,
        )
        user = User.objects.get(kakao_id=kakao_id)
        auth.login(request, user)
    return redirect('/')

