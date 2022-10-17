from django.shortcuts import render, redirect
from django.http import HttpResponse



def detail_comment(request):

    return HttpResponse('게시글 읽기')



def write_comment(request):
    
    return HttpResponse('게시글 등록')



def delete_comment(request):
    
    return HttpResponse('게시글 삭제')


