import torch
import ultralytics
from ultralytics import YOLO

print(f"Number of GPUs available: {torch.cuda.device_count()}")

model = YOLO('runs/detect/train7/weights/best.pt')

# results = model.predi
# yolo task=detect mode=predict model=runs/detect/yolov8n_v8_50e/weights/best.pt source=inference_data/video_1.mp4 show=True imgsz=1280 name=yolov8n_v8_50e_infer1280 hide_labels=True