import torch
import numpy as np
import cv2
import os

import pathlib

# https://www.youtube.com/watch?v=tFNJGim3FXw&ab_channel=NicholasRenotte
# Tutorial used to create this program

# Fixing path bug i encountered requiring unix or linux based system by converting to windows
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# PyTorch function used to load models.
# Trained using YOLOv5 using a custom dataset of gestures
# YOLOv5 model by Ultralytics https://github.com/ultralytics/yolov5
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/yolov5s_gestures_final_v2/weights/best.pt', force_reload=True)

# Output of algorithm to be used as output to game
label_names_list = model.names
current_detection = None
gesture_history = []

# OpenCV camera video capture
cap = cv2.VideoCapture(0)
while cap.isOpened():
    
    ret, frame = cap.read()
    try:
        results = model(frame)
        
        # Box positioning using xyxy
        cv2.imshow('Gesture Detection', np.squeeze(results.render()))

        # All detections put into a list of labels
        labels = [label_names_list[int(i.cpu().numpy())] for i in results.xyxy[0][:, -1].int()]
        # Set first-most label as current detection
        current_detection = labels[0] if labels else None
        print("\n", current_detection)
        
        # Create logfile to see most identified gestures
        # used to fix any bias/skewing
        if current_detection:
            gesture_history.append(current_detection)
            if os.path.isfile("gesture_history.txt"):
                with open('gesture_history.txt', 'w') as file:
                    file.write("\n".join(gesture_history))
            else:
                with open('gesture_history.txt', 'a') as file:
                    file.write("\n".join(gesture_history))
    except Exception as e:
        print("Error given: ", e)

    # Break if keyboard q is pressed
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()