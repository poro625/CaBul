from django.urls import path
from . import views

app_name = 'contents'

urlpatterns = [
    path('upload/', views.Upload, name='upload'),
    path('detail/<int:id>', views.FeedDetail, name='detail_feed'),
    path('search/', views.search, name='search'),
    path('detail/comment/<int:id>',views.write_comment, name='write_comment'), # 댓글 쓰기
    path('detail/comment/delete/<int:feed_id>',views.delete_comment, name='delete_comment'), # 해당 삭제
]

