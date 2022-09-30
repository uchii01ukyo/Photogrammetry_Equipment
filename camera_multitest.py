# coding: UTF-8
import cv2
import os
import time

i = 0
flag = True
captures = []

dir = "./capture"
if not os.path.exists(dir):
    os.makedirs(dir)

while( flag ):
    capture = cv2.VideoCapture(i)
    ret, frame = capture.read()
    flag = ret
    if flag:
       i += 1
       #captures.append( capture )

while(True):
    start = time.time()
    key = cv2.waitKey(1) & 0xFF
    if key == ord(' '):
        break

    for i, capture in enumerate( captures ):
        ret, frame = capture.read()
        #cv2.imshow( 'frame' + str(i), frame )

        path="./capture/camera"
        cv2.imwrite('{}_{}.{}'.format(path, i, 'jpg'), frame)

    print(time.time() - start)
    time.sleep(5)

capture.release()