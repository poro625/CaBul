from unicodedata import name
from django.urls import path
from . import views
from .views import *

app_name='contents'
urlpatterns = [
    
    path("", views.index, name="index"),
    path("<int:feed_id>/", views.post_detail ,name="post_detail"),
    path("<int:feed_id>/delete/", views.post_delete ,name="post_delete"),
    path("post/", views.post,name="post"),
    path('<int:feed_id>/edit/',views.post_edit, name='post_edit'),
    path('<int:feed_id>/update/',views.post_update, name='post_update'),
    
      
]