# coding: UTF-8
import cv2
import os

# esp = break, c = capture
cap = cv2.VideoCapture(0)

# os.makedirs(dir_path, exist_ok=True)
# base_path = os.path.join(dir_path, basename)

n = 0
while True:
    ret, frame = cap.read()

    height = frame.shape[0]
    width = frame.shape[1]
    resized_frame = cv2.resize(frame,(width/2, height/2))

    cv2.imshow('framename', resized_frame)

    key = cv2.waitKey(10)
    if key == ord('c'):
        cv2.imwrite('{}_{}.{}'.format('camera_capture', n, 'jpg'), frame)
        n += 1
    elif key == 27:
        break

cap.release()
cv2.destroyWindow('framename')