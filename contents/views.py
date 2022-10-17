from django.shortcuts import render, redirect
from users.models import User

# Create your views here.

def Upload(request):
    if request.method == 'GET':  # 요청하는 방식이 GET 방식인지 확인하기
        return render(request, 'upload.html')

    if request.method == 'POST':
        my_feed = Feed()  # 글쓰기 모델 가져오기
        my_feed.user = models.ForeignKey('users.User', on_delete = models.CASCADE)  # 모델에 사용자 저장
        my_feed.content = request.POST.get('content', '')  # 모델에 글 저장
        my_feed.like = 0
        my_feed.image = "https://i1.ruliweb.com/img/22/10/04/1839e60028750ad5d.jpg"
        my_feed.category = request.POST.get('category', '') # 모델에 카테고리 저장
        my_feed.tags = request.POST.get('tag', '').split(',')
        for tag in tags:
            tag = tag.strip()
            if tag != '': # 태그를 작성하지 않았을 경우에 저장하지 않기 위해서
                my_feed.tags.add(tag)
        my_feed.save()
        my_feed.save()
        return redirect('/')