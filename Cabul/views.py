from django.shortcuts import render, redirect


# Create your views here.

def home(request):
    if request.method == 'GET':
        user = request.user.is_authenticated  # 사용자가 로그인이 되어 있는지 확인하기
        if user:  # 로그인 한 사용자라면
            return render(request, 'home.html')
        
        else:  # 로그인이 되어 있지 않다면
            return redirect('/users/login')