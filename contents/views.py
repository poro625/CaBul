from multiprocessing import context
from os import posix_spawn
import re
from turtle import title
from django.forms import FileField
from django.http import HttpResponse
from contents.models import Feed
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required


def index(request):
    feeds= Feed.objects.all().order_by("-created_at")
    context = {
        "feeds":feeds
    }

    return render(request,"index.html", context)

def post(request):
    if request.method =="GET":
        return render(request, "post.html")
    elif request.method == "POST":
        title =request.POST.get("title")
        content =request.POST.get("content")
        user =request.user
        Feed.objects.create(title=title, content=content, user =user)
        return redirect("contents:index")
        
    
def post_detail(request, feed_id):
    post = get_object_or_404(Feed,id=feed_id)
    context = {
        "post":post
    }
    return render(request, "post_detail.html", context)

def post_delete(request, feed_id):
    post =Feed.objects.get(id=feed_id)
    post.delete()
    return redirect('/contents')
    
    
def post_edit(request, feed_id):
    post = Feed.objects.get(id=feed_id)
    context = {
        'post': post,
    }
    return render(request, 'edit.html', context)


def post_update(request, feed_id):
    post = Feed.objects.get(id=feed_id)
    post.title = request.POST.get('title')
    post.content = request.POST.get('content')
    post.save()
    
    return redirect ('contents:post_detail', post.id)

