from django.urls import path
from . import views

app_name = 'contents'

urlpatterns = [
    path('upload/', views.Upload, name='upload'),
    path('detail/<int:id>', views.FeedDetail, name='detail_feed'),
    path('search/', views.search, name='search'),
    path('<int:feed_id>/',views.detail_comment,name='detail_comment'), # 댓글 읽기
    path('comment/<int:feed_id>',views.write_comment, name='write_comment'), # 댓글 쓰기
    path('comment/delete/<int:feed_id>',views.delete_comment, name='delete_comment'), # 해당 삭제
    path('<int:feed_id>/likes/', views.likes, name='likes'), # 좋아요 
]

