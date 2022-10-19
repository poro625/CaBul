from django.http import HttpResponse
import torch
from django.http import HttpResponse

def yolo(img, my_feed):
    try:
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        imgs = [(f'./media/{img}')] # batch of images

        results = model(imgs)
        
        category_name = results.pandas().xyxy[0]['name'][0]
        my_feed.category = category_name
        my_feed.save()
    except(IndexError):
        category_name = '카테고리 없음'
        my_feed.category = category_name
        my_feed.save()
        