from unicodedata import category

from gc import get_objects

from contents.models import Feed, Comment

from django.shortcuts import HttpResponse, get_object_or_404, redirect, render

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView
from django.contrib import messages
from django.db.models import Q
# import torch
# import cv2
from .Classification import update_category, upload_category



@login_required 
def post(request):
    if request.method =="GET":
        return render(request, "upload.html")

    elif request.method == "POST":
        my_feed = Feed()
        my_feed.title =request.POST.get("title")
        my_feed.content =request.POST.get("content")
        my_feed.user =request.user
        my_feed.like = 0
        my_feed.image = request.FILES['feed_image']
        my_feed.save()
        
        img = my_feed.image
        upload_category(img, my_feed)
        
        tags = request.POST.get('tag', '').split(',')
        for tag in tags:
            tag = tag.strip()
            if tag != '': # 태그를 작성하지 않았을 경우에 저장하지 않기 위해서
                my_feed.tags.add(tag)
        return redirect('/')

        
    
def post_detail(request, id):
    my_feed = Feed.objects.get(id=id)

    comment = Comment.objects.filter(feed_id=id).order_by('created_at')

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

    same_feed_categorys = Feed.objects.filter(category=my_feed.category)

    context = {
        'feeds':my_feed,
        'comments': comment,
        'feed_count_all':feed_count_all,
        'categorys' : feed_categorys,
        'same_feed_categorys' :same_feed_categorys
    }
    return render(request, 'index.html', context)

def post_delete(request, id):
    post = Feed.objects.get(id=id)
    post.delete()
    return redirect('/')
    
    
def post_edit(request, id):
    post = Feed.objects.get(id=id)
    context = {
        'post': post,
    }
    return render(request, 'update.html', context)


def post_update(request, id):
    if request.method == "GET":
        post = Feed.objects.get(id=id)
        return render(request, 'update.html', {"post":post})

    if request.method == "POST":
        post = Feed.objects.get(id=id)
        post.title = request.POST.get('title', '')
        post.content = request.POST.get('content', '')
        post.image = request.FILES['image']
        post.save()
        
        img = post.image
        update_category(img, post)
        
        return redirect('contents:post_detail', id)



class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = Feed

    def get_queryset(self):
        return Feed.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context


def search(request):
    q = request.POST.get('q', "")  # I am assuming space separator in URL like "random stuff"
    search_menu = request.POST.get('search_menu', "")
    feed_cate = Feed.objects.all().order_by('-category')
    feed_category = feed_cate.values_list('category', flat=True).distinct()
    print(search_menu)
    if search_menu == '1':
        query = Q(title__icontains=q)
        searched = Feed.objects.filter(query)

    elif search_menu == '2':
        query = Q(content__icontains=q)
        searched = Feed.objects.filter(query)

    elif search_menu == '3':
        query = Q(tags__name__icontains=q)
        searched = Feed.objects.filter(query)

    
    elif search_menu == '4':
        query = Q(category__icontains=q)
        searched = Feed.objects.filter(query)
    else :
        return redirect('/')
    
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
        'searched':searched,
        'q': q,
        'feed_count_all':feed_count_all,
        'categorys' : feed_categorys
        }
    return render(request, 'search.html', context)


def write_comment(request, id): # 댓글 쓰기
    if request.method == 'POST':
        current_comment = Feed.objects.get(id=id)
        comment = request.POST.get('comment')

        FC = Comment()
        FC.comment = comment
        FC.user = request.user
        FC.feed = current_comment
        FC.save()

    return redirect('contents:post_detail', id)


def delete_comment(request, feed_id): # 댓글 삭제
    if request.method == 'POST':
        comment = Comment.objects.get(id= feed_id)        
        if comment.user == request.user:
            comment.delete()
            return redirect('contents:post_detail', id)
        else:
            return HttpResponse('권한이 없습니다!')




