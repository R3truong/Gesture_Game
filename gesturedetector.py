import torch
import numpy as np
import cv2

import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp4/weights/best.pt', force_reload=True)

device = torch.device(0)
model.to(device)
print(device)

class_names = model.names

current_detection = None

cap = cv2.VideoCapture(0)
while cap.isOpened():
    
    ret, frame = cap.read()
    results = model(frame)
    cv2.imshow('Gesture Detection', np.squeeze(results.render()))


    labels = [class_names[int(i.cpu().numpy())] for i in results.xyxy[0][:, -1].int()]

    current_detection = labels[0] if labels else None
    print("\n")
    print("\n")
    print("\n")
    print(current_detection)
    print("\n")
    print("\n")
    print("\n")


    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()