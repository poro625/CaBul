import torch

def upload_category(img, my_feed):
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

def update_category(img, post):
    try:
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        imgs = [(f'./media/{img}')] # batch of images

        results = model(imgs)
        
        category_name = results.pandas().xyxy[0]['name'][0]
        post.category = category_name
        post.save()
    except(IndexError):
        category_name = '카테고리 없음'
        post.category = category_name
        post.save()