from django.urls import path
from . import views

app_name='contents'

urlpatterns = [
    path('upload/', views.Upload,name='upload'),
]