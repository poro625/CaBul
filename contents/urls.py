from django.urls import path
from . import views

app_name='contents'
urlpatterns = [
    path("delete/<int:id>", views.post_delete ,name="post_delete"),
    path("post/", views.post,name="post"),
    path('detail/<int:id>', views.post_detail, name='post_detail'),
    path('update/<int:id>', views.post_update, name='post_update'),
    path('search/', views.search, name='search'),

    # path('detail/comment/<int:id>',views.write_comment, name='write_comment'), # 댓글 쓰기
    # path('detail/comment/delete/<int:id>',views.delete_comment, name='delete_comment'), # 해당 삭제

    path('<int:feed_id>/',views.detail_comment,name='detail_comment'), # 댓글 읽기
    path('comment/<int:feed_id>',views.write_comment, name='write_comment'), # 댓글 쓰기

    path('comment/delete/<int:feed_id>',views.delete_comment, name='delete_comment'), # 해당 삭제

    path('<int:feed_id>/likes/', views.likes, name='likes'), # 좋아요 

]

