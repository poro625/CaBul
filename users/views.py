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
        if password != password2:
            return render(request, 'signup.html')
        else:
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'signup.html')
            else:
                UserModel.objects.create_user(username=username, password=password, email=email, nickname=nickname)
                return redirect('/sign-in') # 회원가입이 완료되었으므로 로그인 페이지로 이동


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