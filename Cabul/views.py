from django.shortcuts import render, redirect
from contents.models import Feed


# Create your views here.

def home(request): # home 화면
    if request.method == 'GET' :
        user = request.user.is_authenticated  # 사용자가 인증을 받았는지 (로그인이 되어있는지)
        if user:
            feed = Feed.objects.all().order_by('-created_at')
            feed_cate = Feed.objects.all().order_by('-category')
            feed_category = feed_cate.values_list('category', flat=True).distinct()
            return render(request, 'home.html', { 'feeds' : feed, 'categorys' : feed_category })
        else:
            return redirect('users/login')

def category_view(request, id):
    if request.method == 'GET':
        my_feed = Feed.objects.filter(category=id)
        context = {
            'feeds':my_feed
        }

        return render(request, 'category.html', context)

