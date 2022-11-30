# coding: UTF-8
from __future__ import print_function
import cv2
import os
import time
import threading
import keyboard
import socket
import shutil
from contextlib import closing


captures_ID = []
FRAME_WIDTH=1920
FRAME_HEIGHT=1080
BRIGHTNESS=30

def main():
    # make main directory
    make_directory("./capture")
    make_directory("./connect")

    # camera detection
    print("--- 1. Detection ---")
    detection()

    # camera selection
    # print("----- 2. Selection ------")
    # selection()

    # initial
    global time_start, thread, captures
    time_start=time.time()
    thread=[0]*(len(captures_ID)+1)
    captures=[0]*(len(captures_ID)+1)
    # clear text
    f = open("waiting.txt","w")
    f.close()

    print("Connecting ... " + str(len(captures_ID)))
    print("--- 3. connection ---")

    # capture (select one of the following)
    # mode_movie()
    mode_picture()
    # mode_autoPicture()

    # multithread join
    for ID in captures_ID:
        thread[ID].join()
    
    print(" ")
    print("All completed successfully!")


def camera_connect_waiting():
    while True:
        dir="./connect"
        rows=sum(os.path.isfile(os.path.join(dir, name)) for name in os.listdir(dir))
        if rows==len(captures_ID):
            f = open('waiting.txt', 'w')
            f.write('OK')
            f.close()
            break
        time.sleep(0.1)
    print("-------------------")
    print("All connected.")


def set_multithread(target):
    for ID in captures_ID:
        th=threading.Thread(target=target, name="camera" + str(ID), args=(ID,captures,))
        thread[ID]=th
        thread[ID].start()


def mode_movie():
    set_multithread(camera_capture_movie)
    camera_connect_waiting()
    print(" ")
    print("frame size: " + str(FRAME_WIDTH) + " x " + str(FRAME_HEIGHT))
    print(" ")
    print("c = capture, esc = exit")

    while True:
        if keyboard.read_key() == "c":
            print("Push c -> capture")
            time0=time.time()
            f = open('waiting.txt', 'w')
            f.write("c")
            f.close()
            break
    while True:
        if keyboard.read_key() == "esc":
            print("Push esc -> exit")
            f = open('waiting.txt', 'w')
            f.write("esc")
            f.close()
            break


def mode_picture():
    set_multithread(camera_capture_picture)
    camera_connect_waiting()
    print(" ")
    print("frame size: " + str(FRAME_WIDTH) + " x " + str(FRAME_HEIGHT))
    print(" ")
    print("c = capture, esc = exit")
    while True:
        if keyboard.read_key() == "c":
            f = open('waiting.txt', 'w')
            f.write("c")
            f.close()
            time.sleep(1)
            f = open('waiting.txt', 'w')
            f.write(" ")
            f.close()
        elif keyboard.read_key() == "esc":
            f = open('waiting.txt', 'w')
            f.write("esc")
            f.close()
            break
        time.sleep(2)


def mode_autoPictute():
    set_multithread(camera_capture_picture)
    camera_connect_waiting()
    print("c = capture, esc = exit")
    print("autoPicture")


def camera_setting(cap):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, BRIGHTNESS)
    #camera_setting_show(cap)


def camera_setting_show(cap):
    print("FRAME_WIDTH  : " + str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print("FRAME_HEIGHT : " + str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("FPS          : " + str(cap.get(cv2.CAP_PROP_FPS)))
    print("BRIGHTNESS   : " + str(cap.get(cv2.CAP_PROP_BRIGHTNESS)))
    print("CONTRAST     : " + str(cap.get(cv2.CAP_PROP_CONTRAST)))
    print("SATURATION   : " + str(cap.get(cv2.CAP_PROP_SATURATION)))
    print("HUE          : " + str(cap.get(cv2.CAP_PROP_HUE)))
    print("GAIN         : " + str(cap.get(cv2.CAP_PROP_GAIN)))
    print("EXPOSURE     : " + str(cap.get(cv2.CAP_PROP_EXPOSURE)))


def camera_capture_movie(ID, captures):
    
    # connect
    captures[ID] = cv2.VideoCapture(ID) #(ID,cv2.CAP_DSHOW) 
    if captures[ID].isOpened():
        print("ID: " + str(ID) + " -> Connected")
    else:
        print("ID: " + str(ID) + " -> Failed")

    # camera setting
    camera_setting(captures[ID])

    # mp4 setting
    fps = int(captures[ID].get(cv2.CAP_PROP_FPS))
    w = int(captures[ID].get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(captures[ID].get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')        # fourcc - mp4
    video = cv2.VideoWriter('capture/video_' + str(ID) + '.mp4', fourcc, fps, (w, h))  # filename, fourcc, fps, size

    f = open('connect/camera' + str(ID) + '.txt', 'w')
    f.close()

    # wait
    wait_setting()
    # wait
    while True: 
        f = open('waiting.txt', 'r')
        data = f.read()
        f.close()
        if data=='c':
            break

    # capture
    while True:
        ret, frame = captures[ID].read()
        #cv2.imshow('camera', frame)
        video.write(frame)
        f = open('waiting.txt', 'r')
        data = f.read()
        f.close()
        if data == 'esc':
            break
    captures[ID].release()


def camera_capture_picture(ID, captures):

    # connect
    captures[ID] = cv2.VideoCapture(ID) #(ID,cv2.CAP_DSHOW) 
    if captures[ID].isOpened():
        print("ID: " + str(ID) + " -> Connected")
    else:
        print("ID: " + str(ID) + " -> Failed")

    # camera setting
    camera_setting(captures[ID])

    f = open('connect/camera' + str(ID) + '.txt', 'w')
    f.close()

    # wait
    wait_setting()

    # capture
    n=0
    while True: 
        f = open('waiting.txt', 'r')
        data = f.read()
        f.close()
        if data=='c':
            ret, frame = captures[ID].read()
            cv2.imwrite('{}_{}_{}.{}'.format('capture/camera', ID, n, 'png'), frame)
            print("ID: " + str(ID) + "-> capture")
            n += 1
            time.sleep(2)
        elif data == 'esc':
            break
    captures[ID].release()


def detection():
    print("detects connected cameras.")
    ID=0
    while True:
        capture = cv2.VideoCapture(ID) #cv2.CAP_DSHOW
        if capture.isOpened():
            print("ID: " + str(ID) + " -> Found")
            captures_ID.append(ID)
            ID+=1
        else:
            break
        capture.release()
    print("-------------------")


def selection():
    # detection()
    print("select cameras.")
    check_camera()
    delete_camera()
    print("------------------")


def check_camera():
    while True:
        print("check: Input [check ID] or [esc])")
        input_key=input()
        if input_key=='esc':
            break
        if int_check(input_key):
            input_int=int(input_key)
            capture = cv2.VideoCapture(input_int) #cv2.CAP_DSHOW
            if capture.isOpened():
                print("set up camera ID: " + str(input_int))
                print("* exit: frame windows -> esc")
                while True:
                    ret, frame = capture.read()
                    resized_frame = cv2.resize(frame,(frame.shape[1], frame.shape[0]))
                    cv2.imshow(str(input_int), resized_frame)
                    key = cv2.waitKey(10)
                    if key == 27: # esc
                        break
                capture.release()
                cv2.destroyWindow('framename')
                print("release camera ID: " + str(input_int))
            else:
                print("Input is invalid.")
                break
            capture.release()
        else:
            print("Input is invalid.")
    print("-------------------")


def delete_camera():
    while True:
        print("delete: Input [check ID] or [esc])")
        input_key=input()
        if input_key=='esc':
            break
        if int_check(input_key):
            input_int=int(input_key)
            if captures_ID.count(input_int):
                captures_ID.remove(input_int)
                print(captures_ID)
            else:
                print("The camera ID was not detected.")
        else:
            print("Input is invalid.")
    print("-------------------")

def wait_setting():
    while True: 
        f = open('waiting.txt', 'r')
        data = f.read()
        f.close()
        if(data=='OK'):
            break
        time.sleep(0.1) # waiting


def make_directory(dir):
    print("create a directory, " + str(dir))
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)


def int_check(check_num):
    try:
        int(check_num)
    except ValueError:
        return False
    else:
        return True


if __name__ == '__main__':
   main()