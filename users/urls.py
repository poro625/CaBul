from django.urls import path
from . import views

app_name='users'

urlpatterns = [
    path('signup/', views.signup,name='signup'),
    path('login/', views.login,name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/<int:id>/', views.update, name='update'),
    path('password/<int:id>', views.password, name='password'),
    path('delete/', views.delete, name='delete'),
    
]