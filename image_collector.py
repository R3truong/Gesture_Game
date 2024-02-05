import cv2
import uuid
import os
import time

IMAGES_PATH = os.path.join('data', 'images')
labels = ['point_right', 'point_left']
numbers_imgs = 5

cap = cv2.VideoCapture(0)
for label in labels:
    print('collecting pictures for {}'.format(labels))
    time.sleep(5)
    for img_num in range(numbers_imgs):
        print('Collecting images for {}, image number {}'.format(label,img_num))
        imgname = os.path.join(IMAGES_PATH, label+'.'+str(uuid.uuid1())+'.jpg')
        ret, frame = cap.read()
        cv2.imwrite(imgname, frame)
        cv2.imshow("Image Collection", frame)
        time.sleep(2)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
