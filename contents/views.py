from contents.models import Feed, Comment
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView
from django.contrib import messages
from django.db.models import Q

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
        my_feed.category = request.POST.get('category', '')
        my_feed.save()
        tags = request.POST.get('tag', '').split(',')
        for tag in tags:
            tag = tag.strip()
            if tag != '': # 태그를 작성하지 않았을 경우에 저장하지 않기 위해서
                my_feed.tags.add(tag)
        return redirect('/')

        
    
def post_detail(request, id):
    my_feed = Feed.objects.get(id=id)
    comment = Comment.objects.filter(feed_id=id).order_by('-created_at')
    context = {
        'feeds':my_feed,
        'comments': comment
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
        post.save()
        
        return redirect('contents:post_detail', post.id)

# @login_required
# def Upload(request):
#     if request.method == 'GET':  # 요청하는 방식이 GET 방식인지 확인하기
#         return render(request, 'upload.html')

#     if request.method == 'POST':
#         user = request.user
#         my_feed = Feed()  # 글쓰기 모델 가져오기
#         my_feed.user = user
#         my_feed.title = request.POST.get('title', '')  # 모델에 글 저장
#         my_feed.content = request.POST.get('content', '')  # 모델에 글 저장
#         my_feed.like = 0
#         my_feed.image = "https://i1.ruliweb.com/img/22/10/04/1839e60028750ad5d.jpg"
#         my_feed.category = request.POST.get('category', '') # 모델에 카테고리 저장
#         my_feed.save()
#         tags = request.POST.get('tag', '').split(',')
#         for tag in tags:
#             tag = tag.strip()
#             if tag != '': # 태그를 작성하지 않았을 경우에 저장하지 않기 위해서
#                 my_feed.tags.add(tag)
#         return redirect('/')


# def FeedDetail(request, id):
#     my_feed = Feed.objects.get(id=id)
#     comment = Comment.objects.filter(feed_id=id).order_by('-created_at')
#     return render(request, 'index.html', {'feeds':my_feed, 'comments': comment})


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


    return render(request, 'search.html',{'searched':searched, 'q': q })


# def detail_comment(request, id ): # 댓글 읽기
#     my_feed = Feed.objects.get(id=id)
#     comment = Comment.objects.filter(tweet_id=id).order_by('-created_at')

#     return render(request,'index.html', my_feed=my_feed, comment=comment )



def write_comment(request, id): # 댓글 쓰기
    if request.method == 'POST':
        current_comment = Feed.objects.get(id=id)
        comment = request.POST.get('comment')

        FC = Comment()
        FC.comment = comment
        FC.user = request.user
        FC.feed = current_comment
        FC.save()

    return redirect('/')



def delete_comment(request, id ): # 댓글 삭제
    
    feed = Feed.objects.get(id=id)
    comment = request.POST.get('comment')
    feed.delete()
    return redirect('/')
