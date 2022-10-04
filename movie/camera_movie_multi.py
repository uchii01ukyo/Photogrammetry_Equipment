# coding: UTF-8
import cv2
import os
import time
import threading
import keyboard

captures_ID = []

def main_multithread():

    # make main directory
    dir = "./capture"
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    # camera detection
    detection()

    # initial
    time_start=time.time()
    thread=[len(captures_ID)]
    captures=[0]*(len(captures_ID)+1)
    # clear text
    f = open("waiting.txt","w")
    f.close()

    print("Connecting ... " + str(len(captures_ID)))
    print("---connection---")
    for ID in captures_ID:
        th=threading.Thread(target=camera_capture, name="camera" + str(ID), args=(ID,captures,time_start,))
        thread[ID]=th
        thread[ID].start()

    while True:
        rows=sum([1 for _ in open('waiting.txt')])
        if rows==len(captures_ID):
            f = open('waiting.txt', 'w')
            f.write('OK')
            f.close()
            break
        time.sleep(0.1)
    print("-----------------")

    print("Recording ... exit = esc")
    
    for ID in captures_ID:
        thread[ID].join()
    
    print("All completed successfully!")



def camera_capture(ID, captures, time_start):
    captures[ID] = cv2.VideoCapture(ID)
    if captures[ID].isOpened():
        print("ID: " + str(ID) + " -> Connected")
    else:
        print("ID: " + str(ID) + " -> Failed")

    fps = int(capture.get(cv2.CAP_PROP_FPS))
    w = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')        # fourcc - mp4
    video = cv2.VideoWriter('video_' + str(ID) + '.mp4', fourcc, fps, (w, h))  # filename, fourcc, fps, size

    f = open('waiting.txt', 'a')
    f.write(str(ID) + '\n')
    f.close()

    # wait
    wait_setting()

    while True:
        ret, frame = captures[ID].read()
        #cv2.imshow('camera', frame)
        video.write(frame)
        if keyboard.is_pressed('escape'):
            break
    captures[ID].release()


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


def wait_setting():
    while True: 
        f = open('waiting.txt', 'r')
        data = f.read()
        f.close()
        if(data=='OK'):
            break
        time.sleep(0.1) # waiting

if __name__ == '__main__':
    main_multithread()