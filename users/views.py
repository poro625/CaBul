from django.shortcuts import render, redirect
from .models import User
from contents.models import Feed
from django.contrib.auth import authenticate, login as loginsession
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from contents.models import Feed
from django.contrib import auth

import re
import requests

# SMTP 관련 인증
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token


# Create your views here.
def signup(request): # 회원가입
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
                user= User.objects.create_user(email=email, username=username, password=password, nickname=nickname, profile_image=profile_image)
                user.is_active = False # 유저 비활성화
                user.save()
                current_site = get_current_site(request)
                message = render_to_string('activation_email.html', {
                    'user':user,
                    'domain':current_site.domain, 
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),

                })
                mail_title = "계정 활성화 확인 이메일"
                mail_to = request.POST["email"]
                email = EmailMessage(mail_title, message, to=[mail_to])
                email.send()

                return render(request, 'login.html') # 회원가입이 완료되었으므로 로그인 페이지로 이동

# 계정 활성화 함수(토큰을 통해 인증)
def activate(request, uidb64, token): # 계정 활성화
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExsit):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect("/")
    else:
        return render(request, 'home.html', {'error' : '계정 활성화 오류'})

def login(request): #로그인
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'login.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email , password=password)
        if user is not None:
            loginsession(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error':'이메일 인증 or 이메일 패스워드를 확인해 주세요!'})

@login_required
def logout(request):   #로그아웃 
    auth.logout(request) # 인증 되어있는 정보를 없애기
    return redirect("/")

@login_required
def delete(request):   #회원탈퇴
    if request.user.is_authenticated:
        request.user.delete()
    return render(request, 'signup.html')


def update(request, id): # 회원정보 수정
    if request.method == 'GET':# 프로필 수정 페이지 접근
        user_feed = Feed.objects.filter(user_id=request.user.id)
        user_feed_count = len(user_feed)

        feed = Feed.objects.all().order_by('-created_at')
        feed_count_all = len(feed)
        feed_cate = Feed.objects.all().order_by('-category')
        feed_category_all = feed_cate.values_list('category', flat=True)
        feed_category = feed_cate.values_list('category', flat=True).distinct()
        feed_categorys = []
        for cate in feed_category:
            cate_count = 0
            for i in feed_category_all:
                if cate == i:
                    cate_count += 1
            feed_categorys.append({
                'category' : cate,
                'cate_count' : cate_count
            })
        context = {
            'feed_count_all':feed_count_all,
            'categorys' : feed_categorys,
            'user_feed_count' : user_feed_count
        }
        return render(request, 'profile_edit.html', context)
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
    
def profileupload(request, id): # 프로필 사진 수정
    if request.method == 'GET':
        user_feed = Feed.objects.filter(user_id=request.user.id)
        user_feed_count = len(user_feed)

        feed = Feed.objects.all().order_by('-created_at')
        feed_count_all = len(feed)
        feed_cate = Feed.objects.all().order_by('-category')
        feed_category_all = feed_cate.values_list('category', flat=True)
        feed_category = feed_cate.values_list('category', flat=True).distinct()
        feed_categorys = []
        for cate in feed_category:
            cate_count = 0
            for i in feed_category_all:
                if cate == i:
                    cate_count += 1
            feed_categorys.append({
                'category' : cate,
                'cate_count' : cate_count
            })
        context = {
            'feed_count_all':feed_count_all,
            'categorys' : feed_categorys,
            'user_feed_count' : user_feed_count
        }
        return render(request, 'profileupload.html', context)
    elif request.method =='POST':
        user = User.objects.get(id=id)
        user.profile_image = request.FILES['image']
        
        user.save()
        return render(request, 'profileupload.html')

def password(request, id): # 비밀번호

    if request.method == 'GET':# 프로필 수정 페이지 접근
        user_feed = Feed.objects.filter(user_id=request.user.id)
        user_feed_count = len(user_feed)

        feed = Feed.objects.all().order_by('-created_at')
        feed_count_all = len(feed)
        feed_cate = Feed.objects.all().order_by('-category')
        feed_category_all = feed_cate.values_list('category', flat=True)
        feed_category = feed_cate.values_list('category', flat=True).distinct()
        feed_categorys = []
        for cate in feed_category:
            cate_count = 0
            for i in feed_category_all:
                if cate == i:
                    cate_count += 1
            feed_categorys.append({
                'category' : cate,
                'cate_count' : cate_count
            })
        context = {
            'feed_count_all':feed_count_all,
            'categorys' : feed_categorys,
            'user_feed_count' : user_feed_count
        }
        return render(request, 'profile_edit_password.html', context)

    elif request.method == 'POST':
        user = User.objects.get(id=id)
        origin_password = request.POST["origin_password"]
        check = check_password(origin_password, user.password)
        if check:
            new_password = request.POST["new_password"]
            confirm_password = request.POST["confirm_password"]
            
            if new_password != confirm_password:
                return render(request, 'profile_edit_password.html', {'error':'새 비밀번호를 확인해주세요.'})
            elif (len(new_password) < 8):
                return render(request, 'profile_edit_password.html', {'error': '패스워드는 8자 이상이어야 합니다!'})
            elif re.search('[a-zA-z]+', new_password)is None:
                return render(request, 'profile_edit_password.html', {'error': '비밀번호는 최소 1개 이상의 영문이 포함되어야 합니다!'})
            elif re.search('[0-9]+', new_password) is None:
                return render(request, 'profile_edit_password.html', {'error': '비밀번호에는 최소 1개 이상의 숫자가 포함되어야 합니다!'})
            elif re.search('[`~!@#$%^&*(),<.>/?]+', new_password) is None:
                return render(request, 'profile_edit_password.html', {'error': '비밀번호에는 최소 1개 이상의 특수문자가 포함되어야 합니다!'})
            else:
                user.set_password(new_password)
                user.save()
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return render(request,'profile_edit_password.html' )
        else:
            return render(request, 'profile_edit_password.html', {'error':'비밀번호가 일치하지 않습니다'})
        
@login_required
def user_view(request): #
    if request.method == 'GET':

        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = User.objects.all().exclude(email=request.user.email)

        user_feed = Feed.objects.filter(user_id=request.user.id)
        user_feed_count = len(user_feed)

        feed = Feed.objects.all().order_by('-created_at')
        feed_count_all = len(feed)
        feed_cate = Feed.objects.all().order_by('-category')
        feed_category_all = feed_cate.values_list('category', flat=True)
        feed_category = feed_cate.values_list('category', flat=True).distinct()
        feed_categorys = []
        for cate in feed_category:
            cate_count = 0
            for i in feed_category_all:
                if cate == i:
                    cate_count += 1
            feed_categorys.append({
                'category' : cate,
                'cate_count' : cate_count
            })
        context = {
            'user_list': user_list,
            'feed_count_all':feed_count_all,
            'categorys' : feed_categorys,
            'user_feed_count' : user_feed_count
        }
        return render(request, 'follow.html', context)
        


@login_required
def user_follow(request, id):
    me = request.user
    click_user = User.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect(request.META['HTTP_REFERER'])     


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
    profile_image = profile_json['properties']['profile_image']

    if User.objects.filter(kakao_id=kakao_id).exists():
        user = User.objects.get(kakao_id=kakao_id)
        user.kakao_profile = profile_image
        user.save()
        auth.login(request, user)  # 로그인 처리
    else:
        User.objects.create(
            username=username,
            kakao_profile=profile_image,
            kakao_id=kakao_id,
        )
        user = User.objects.get(kakao_id=kakao_id)
        auth.login(request, user)
    return redirect('/')
