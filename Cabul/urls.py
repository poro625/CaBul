"""Cabul URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from users.views import kakao_social_login, kakao_social_login_callback
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), #admin 페이지 접속
    path('users/', include('users.urls')), # users 앱 url 연결
    path('contents/', include('contents.urls')), # contents 앱 url 연결
    path('', views.home, name='home'), # home화면 연결
    path('category/<str:id>', views.category_view, name='category'), # 카테고리 분류 페이지 연결
    path('account/login/kakao/', kakao_social_login, name='kakao_login'), # 카카오 로그인 요청을 보낼 url
    path('account/login/kakao/callback/', kakao_social_login_callback, name='kakao_login_callback'), # 카카오 받은 인가 코드로 접근 토근을 받아 유저의 정보를 가져올 url
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # static 경로 설정

