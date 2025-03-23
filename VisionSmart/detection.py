import cv2
import torch
import numpy as np
from ultralytics import YOLO
from color import detect_color_kmeans
from shopping import get_amazon_best_deal
import pyttsx3

# Load the trained YOLOv12 model
model = YOLO('yolov12_best.pt')

# Dangerous Objects List
DANGEROUS_OBJECTS = {"knife", "lighter", "scissor", "cleaning chemical", "broken socket", "candle", "coin", "glass shard", "needle", "paint thinner"}

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

def detect_objects(frame):
    results = model(frame)
    annotated_frame = results[0].plot()
    detected_objects = []

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy.cpu().numpy()[0])

            class_id = int(box.cls[0])
            object_name = model.names[class_id]

            # Detect object color using K-Means
            object_color = detect_color_kmeans(frame, x1, y1, x2, y2)
            label = f"{object_color} {object_name}"
            detected_objects.append(label)

            # Fetch Amazon deal link
            amazon_link = get_amazon_best_deal(object_name, object_color)
            detected_objects.append(f"Buy Here: {amazon_link}")

            # Danger Alert
            if object_name.lower() in DANGEROUS_OBJECTS:
                cv2.putText(annotated_frame, "⚠ DANGER!", (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                engine.say(f"Warning! A {object_name} is detected!")
                engine.runAndWait()

    return annotated_frame, detected_objects
