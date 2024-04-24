import socket
import torch
import numpy as np
import cv2
import os

import pathlib

host, port = "127.0.0.1", 25001
dataX = 30
dataY = 6
dataZ = 0
running = True
confidenceMin = 0.60
lastDetection = ""

# SOCK_STREAM means TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def sendData(data):
        sock.sendall(data.encode("utf-8"))
        response = sock.recv(1024).decode("utf-8")
        print ("Response: ", response)

# https://www.youtube.com/watch?v=tFNJGim3FXw&ab_channel=NicholasRenotte
# Tutorial used to create this program

# Fixing path bug i encountered requiring unix or linux based system by converting to windows
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# PyTorch function used to load models.
# Trained using YOLOv5 using a custom dataset of gestures
# YOLOv5 model by Ultralytics https://github.com/ultralytics/yolov5
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/yolov5s_gestures_added_gestures_v32/weights/best.pt', force_reload=True)

# Output of algorithm to be used as output to game
label_names_list = model.names
current_detection = None
gesture_history = []

# OpenCV camera video capture
cap = cv2.VideoCapture(0)
try:
      sock.connect((host, port))
      while cap.isOpened():
      
            ret, frame = cap.read()
            results = model(frame)
            
            # Box positioning using xyxy
            cv2.imshow('Gesture Detection', np.squeeze(results.render()))

            # All detections put into a list of labels
            labels = [label_names_list[int(i.cpu().numpy())] for i in results.xyxy[0][:, -1].int()]
            confidences = [float(i.cpu().numpy()) for i in results.xyxy[0][:, 4]]

            # Set first-most label as current detection
            current_detection = labels[0] if labels else None
            current_confidence = confidences[0] if confidences else None
            if current_detection == None:
                current_detection = "None"
                
                current_confidence = 100.0
            
            if(current_detection != lastDetection and current_confidence >= confidenceMin):
                  print("\nSent: ", current_confidence)
                  print("Sent: ", current_detection)
                  lastDetection = current_detection
                  sendData(current_detection)
                  
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
            # Break if keyboard q is pressed
            if cv2.waitKey(10) & 0xFF == ord('q'):
                  sendData("None")
                  break
except Exception as e:
      print("Error given: ", e)
finally:
      sock.close()

cap.release()
cv2.destroyAllWindows()