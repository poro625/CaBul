from django.urls import path
from . import views
from .views import *

app_name='users'

urlpatterns = [
    path('signup/', views.signup,name='signup'),
    path('login/', views.login,name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/<int:id>/', views.update, name='update'),
    path('password/<int:id>', views.password, name='password'),
    path('logout/', views.logout, name='logout'),
    path('user/', views.user_view, name='user-list'),
    path('follow/<int:id>/', views.user_follow, name='follow'),
    path('delete/', views.delete, name='delete'),
    
]