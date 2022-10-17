from django.shortcuts import render, redirect

# Create your views here.

def home(request): # home 화면
    if request.method == 'GET' :
        user = request.user.is_authenticated  # 사용자가 인증을 받았는지 (로그인이 되어있는지)
        if user:
            return render(request, 'home.html')
        else:
            return redirect('users/login')
