from django.urls import path
from . import views

app_name = 'contents'

urlpatterns = [

    path('<int:feed_id>/',views.detail_comment,name='detail_comment'), # 댓글 읽기
    path('comment/<int:feed_id>',views.write_comment, name='write_comment'), # 댓글 쓰기
    path('comment/delete/<int:feed_id>',views.delete_comment, name='delete_comment'), # 해당 삭제
]
