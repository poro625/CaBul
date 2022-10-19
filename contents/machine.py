import torch

def yolo(img, my_feed):

        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        imgs = [(f'./media/{img}')] # batch of images

        results = model(imgs)

        category_name = results.pandas().xyxy[0]['name'][0]

        my_feed.category = category_name
        my_feed.save()