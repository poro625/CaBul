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
    path('detail/<int:id>', views.FeedDetail, name='post_detail'),
    path('update/<int:feed_id>', views.post_edit, name='post_edit'),
    path('<int:feed_id>/update/',views.post_update, name='post_update'),
    path('search/', views.search, name='search'),
    path('detail/comment/<int:id>',views.write_comment, name='write_comment'), # 댓글 쓰기
    path('detail/comment/delete/<int:feed_id>',views.delete_comment, name='delete_comment'), # 해당 삭제
]

