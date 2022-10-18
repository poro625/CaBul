from django.urls import path
from . import views

app_name='contents'

urlpatterns = [
    path('upload/', views.Upload, name='upload'),
    path('detail/<int:id>', views.FeedDetail, name='detail_feed'),
    path('search/', views.search, name='search'),
]