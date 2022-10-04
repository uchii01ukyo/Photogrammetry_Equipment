# coding: UTF-8
import cv2
import os
import time
import threading
import keyboard

captures = []
fps=10

def main_multithread():

    # make main directory
    dir = "./capture"
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    # camera detection
    detection()

    time_start=time.time()
    thread=[len(captures)]
    print("Setting ... " + str(len(captures)))

    for ID in captures:
        thread.append(threading.Thread(target=camera_capture, name="camera" + str(ID), args=(ID, time_start,)))
        thread[ID].start()
    for ID in captures:
        thread[ID].join()


def camera_capture(ID, time_start):
    cap = cv2.VideoCapture(ID) #(ID,cv2.CAP_DSHOW) 
    if cap.isOpened():
        print("ID: " + str(ID) + " -> Success")
    else:
        print("ID: " + str(ID) + " -> Failed")

    n=0
    while True:
        time_last=time.time()
        while True:
            time_frame=time.time()-time_last
            if time_frame*fps>1:
                break
            if keyboard.is_pressed('escape'):
                return
            time.sleep(0.01)

        ret, frame = cap.read()
        cv2.imwrite('{}_{}_{}.{}'.format('camera', ID, n, 'jpg'), frame)
        time_now=time.time()-time_start
        print("ID: " + str(ID) + "-> capture (" + str(time_now) + " sec)")
        n += 1
        
    cap.release()


def detection():
    ID=1
    print("---detection---")
    while True:
        capture = cv2.VideoCapture(ID,cv2.CAP_DSHOW)
        if capture.isOpened():
            print("ID: " + str(ID) + " -> Found")
            captures.append(ID)
            ID+=1
        else:
            break
        capture.release()
    print("---------------")


if __name__ == '__main__':
    #main_simple()
    main_multithread()


"""
def main_simple():
    detection()

    i = 0
    flag = True
    captures = []

    while(flag):
        capture = cv2.VideoCapture(i,cv2.CAP_DSHOW)
        ret, frame = capture.read()
        flag = ret
        if flag:
            i += 1
            captures.append(capture)

    while(True):
        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):
            break

        for i, capture in enumerate(captures):
            ret, frame = capture.read()
            cv2.imshow( 'frame' + str(i), frame )

    capture.release()
    cv2.destroyAllWindows()
"""