from unittest import result
from django.http import HttpResponse
from django.shortcuts import render, redirect
from contents.models import Feed
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

def home(request): # home 화면
    if request.method == 'GET' :
        user = request.user.is_authenticated  # 사용자가 인증을 받았는지 (로그인이 되어있는지)
        if user:
            feed = Feed.objects.all().order_by('-created_at')
            feed_count_all = len(feed)
            
            page = request.GET.get('page')
                
            paginator = Paginator(feed, 12)
            
            try:
                page_obj = paginator.page(page)
            except PageNotAnInteger:
                page = 1
                page_obj = paginator.page(page)
            except EmptyPage:
                page = paginator.num_pages
                page_obj = paginator.page(page)
                
            leftIndex = (int(page) - 2)
            if leftIndex < 1:
                leftIndex = 1
    
            rightIndex = (int(page) + 2)


            user_feed = Feed.objects.filter(user_id=request.user.id)
            user_feed_count = len(user_feed)


            if rightIndex > paginator.num_pages:
                rightIndex = paginator.num_pages
            
            custom_range = range(leftIndex, rightIndex+1)  

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
            return render(request, 'home.html', { 'feeds' : feed, 'categorys' : feed_categorys, 'feed_count_all':feed_count_all, 'page_obj':page_obj, 'paginator':paginator, 'custom_range':custom_range, 'user_feed_count':user_feed_count })
        else:
            return redirect('users/login')


def category_view(request, id): # 카테고리 화면
    if request.method == 'GET':
        my_feed = Feed.objects.filter(category=id)

        feed = Feed.objects.all().order_by('-created_at')
        feed_count_all = len(feed)
        
        user_feed = Feed.objects.filter(user_id=request.user.id)
        user_feed_count = len(user_feed)

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
            'categorys' : feed_categorys,
            'user_feed_count' : user_feed_count
        }

        return render(request, 'category.html', context)


