from django.urls import path
from . import views
from .views import *

app_name='users'

urlpatterns = [
    path('signup/', views.signup,name='signup'), #회원가입
    path('login/', views.login,name='login'), #로그인
    path('logout/', views.logout, name='logout'), #로그아웃
    path('update/<int:id>/', views.update, name='update'), #회원정보수정
    path('password/<int:id>', views.password, name='password'), #비밀번호 변경
    path('profileupload/<int:id>', views.profileupload, name='profileupload'), #프로필 사진 변경
    path('user/', views.user_view, name='user-list'), #팔로우 페이지 창
    path('follow/<int:id>/', views.user_follow, name='follow'), #팔로우. 팔로워
    path('delete/', views.delete, name='delete'), #회원탈퇴
    path('activate/<str:uidb64>/<str:token>/', views.activate, name="activate"), #계정 활성화
    
]