# coding: UTF-8
import cv2
import os
import time
import threading
 
def main_multithread():
    # make main directory
    dir = "./capture"
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    ID=0
    flag = True
    captures = []
    while( flag ):
        capture = cv2.VideoCapture(ID)
        ret, frame = capture.read()
        flag = ret
        if flag:
            captures.append(capture)
            print("VideoCapture(" + str(ID) + ") -> Found")
            ID += 1
    
    t1 = threading.Thread(target=camera_capture, name="camera1", args=(1,))
    t2 = threading.Thread(target=camera_capture, name="camera2", args=(2,))
    t3 = threading.Thread(target=camera_capture, name="camera3", args=(3,))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    print("end")


def camera_capture(ID):
    capture = cv2.VideoCapture(ID)
    fps = int(capture.get(cv2.CAP_PROP_FPS))
    w = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')        # fourcc - mp4
    video = cv2.VideoWriter('video' + str(ID) + '.mp4', fourcc, fps, (w, h))  # filename, fourcc, fps, size

    while True:
        ret, frame = capture.read()
        #cv2.imshow('camera', frame)
        video.write(frame)
        if cv2.waitKey(1)==27:
            break
    capture.release()

if __name__ == '__main__':
    main_multithread()