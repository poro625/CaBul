from unittest import result
from django.http import HttpResponse
from django.shortcuts import render, redirect
from contents.models import Feed


# Create your views here.

def home(request): # home 화면
    if request.method == 'GET' :
        user = request.user.is_authenticated  # 사용자가 인증을 받았는지 (로그인이 되어있는지)
        if user:
            feed = Feed.objects.all().order_by('-created_at')
            feed_count_all = len(feed)

            feed_cate = Feed.objects.all().order_by('-category')
            feed_category_all = feed_cate.values_list('category', flat=True)
            feed_category = feed_cate.values_list('category', flat=True).distinct()
            feed_categorys = []
            for cate in feed_category:
                cate_count = 0
                for i in feed_category_all:
                    if cate == i:
                        cate_count += 1
                feed_categorys.append({
                    'category' : cate,
                    'cate_count' : cate_count
                })
            return render(request, 'home.html', { 'feeds' : feed, 'categorys' : feed_categorys, 'feed_count_all':feed_count_all })
        else:
            return redirect('users/login')


def category_view(request, id):
    if request.method == 'GET':
        my_feed = Feed.objects.filter(category=id)

        feed = Feed.objects.all().order_by('-created_at')
        feed_count_all = len(feed)

        feed_cate = Feed.objects.all().order_by('-category')
        feed_category_all = feed_cate.values_list('category', flat=True)
        feed_category = feed_cate.values_list('category', flat=True).distinct()
        feed_categorys = []
        for cate in feed_category:
            cate_count = 0
            for i in feed_category_all:
                if cate == i:
                    cate_count += 1
            feed_categorys.append({
                'category' : cate,
                'cate_count' : cate_count
            })
        
        context = {
            'feeds':my_feed,
            'feed_count_all':feed_count_all,
            'categorys' : feed_categorys
        }

        return render(request, 'category.html', context)


