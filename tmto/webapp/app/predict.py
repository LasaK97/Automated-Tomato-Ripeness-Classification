from io import BytesIO
from PIL import Image
import cv2
import torch
from ultralytics import YOLO

model = YOLO("models/tmto_model.pt")

def process_image(image_data):
    image = Image.open(BytesIO(image_data))
    results = model(image)
    output_image = results.render()[0]
    buffered = BytesIO()
    Image.fromarray(output_image).save(buffered, format="JPEG")
    return buffered.getvalue()

def process_video(video_path):
    video = cv2.VideoCapture(str(video_path))
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        results = model(frame)
        output_frame = results.render()[0]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', output_frame)[1].tobytes() + b'\r\n')

def process_live_feed(frame_data):
    frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)
    results = model(frame)
    output_frame = results.render()[0]
    return cv2.imencode('.jpg', output_frame)[1].tobytes()
