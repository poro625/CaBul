from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Feed , Comment



def detail_comment(request, id ): # 댓글 읽기
    my_feed = Feed.objects.get(id=id)
    comment = Comment.objects.filter(tweet_id=id).order_by('-created_at')

    return render(request,'index.html', my_feed=my_feed, comment=comment )



def write_comment(request, id ): # 댓글 쓰기
    if request.method == 'POST':
        current_comment = Feed.objects.get(id=id)
        comment = request.POST.get('comment')

        TC = Comment()
        TC.comment = comment
        TC.author = request.user
        TC.tweet = current_comment
        TC.save()

    return redirect('/')



def delete_comment(request, id ): # 댓글 삭제
    
    feed = Feed.objects.get(id=id)
    comment = request.POST.get('comment')
    feed.delete()
    return redirect('/')