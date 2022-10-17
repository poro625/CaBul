from django.urls import path
from . import views

app_name = 'contents'

urlpatterns = [

    path('contents/<int:id>',views.detail_comment,name='detail_comment'), # 댓글 읽어온다
    path('contents/comment/<int:id>',views.write_comment, name='write_comment'), # 댓글 작성하기
    path('tweet/comment/delete/<int:id>',views.delete_comment, name='delete_comment'), # 해당 댓글 삭제
]