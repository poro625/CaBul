from django.urls import path
from . import views

app_name='contents'
urlpatterns = [

    path("delete/<int:id>", views.post_delete ,name="post_delete"), #게시글 삭제
    path("post/", views.post,name="post"), # 게시글 업로드
    path('detail/<int:id>', views.post_detail, name='post_detail'), #게시글 읽기
    path('update/<int:id>', views.post_update, name='post_update'), #게시글 수정
    path('search/', views.search, name='search'), #게시글 검색
    path('detail/comment/<int:id>',views.write_comment, name='write_comment'), # 댓글 쓰기
    path('comment/delete/<int:feed_id>',views.delete_comment, name='delete_comment'), # 해당 삭제
    path('post/likes/<int:id>/', views.likes, name='post_likes'),

]

