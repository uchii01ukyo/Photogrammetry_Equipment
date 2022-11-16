# coding: UTF-8
from __future__ import print_function
import cv2
import os
import time
import threading
#import keyboard
import socket
import shutil
from contextlib import closing


captures_ID = []

def main_multithread():

    # UDP
    UDP_initial()
    print("wait when main device open")
    received=UDP_receive('open','opened')
    
    # make main directory
    dir = "./capture"
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)
    
    # camera detection
    detection()

    # camera selection
    #selection()

    # initial
    time_start=time.time()
    thread=[0]*(len(captures_ID)+1)
    captures=[0]*(len(captures_ID)+1)
    # clear text
    f = open("waiting.txt","w")
    f.close()

    # main-connection
    print("Connecting ... " + str(len(captures_ID)))
    print("--- 3. connection ---")
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
    print("-------------------")
    print("All connected.")

    time.sleep(2)
    while True:
        received=UDP_receive('c','-> capture')
        f = open('waiting.txt', 'w')
        f.write(received)
        f.close()
        print("memo:" + received)
        if received == "esc":
            break
    
    for ID in captures_ID:
        thread[ID].join()
    
    print(" ")
    print("All completed successfully!")


def camera_capture(ID, captures, time_start):
    
    # connect
    captures[ID] = cv2.VideoCapture(ID) #(ID,cv2.CAP_DSHOW) 
    if captures[ID].isOpened():
        print("ID: " + str(ID) + " -> Connected")
    else:
        print("ID: " + str(ID) + " -> Failed")

    fps = int(captures[ID].get(cv2.CAP_PROP_FPS))
    w = int(captures[ID].get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(captures[ID].get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')        # fourcc - mp4
    video = cv2.VideoWriter('capture/video_' + str(ID) + '.mp4', fourcc, fps, (w, h))  # filename, fourcc, fps, size

    f = open('waiting.txt', 'a')
    f.write(str(ID) + '\n')
    f.close()

    # wait1
    wait_setting()
    # wait2
    while True: 
        f = open('waiting.txt', 'r')
        data = f.read()
        f.close()
        if data=='c':
            break
    
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

    # capture
    n=0
    while True: 
        f = open('waiting.txt', 'r')
        data = f.read()
        f.close()
        if data=='c':
            ret, frame = captures[ID].read()
            cv2.imwrite('{}_{}_{}.{}'.format('capture/camera', ID, n, 'jpg'), frame)
            time_now=time.time()-time_start
            print("ID: " + str(ID) + "-> capture (" + str(time_now) + " sec)")
            n += 1
            time.sleep(2)
        elif data == 'esc':
            break
    captures[ID].release()


def detection():
    ID=0
    print("--- 1. Detection ---")
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
    detection()
    print("----- 2. Selection ------")
    print("(1) Input [check ID] or [100])")
    while True:
        input_key=input()
        if int_check(input_key):
            input_int=int(input_key)
            if captures_ID.count(input_int):
                print("Set up Camera ID: " + str(input_int))
                capture = cv2.VideoCapture(input_int) #cv2.CAP_DSHOW
                # capture
                while True:
                    ret, frame = capture.read()
                    resized_frame = cv2.resize(frame,(frame.shape[1]/2, frame.shape[0]/2))
                    cv2.imshow('framename', resized_frame)
                    key = cv2.waitKey(10)
                    if key == 27:
                        break
                print("Release Camera ID: " + str(input_int))
                capture.release()
                cv2.destroyWindow('framename')
            elif input_int == 100:
                break
            else:
                print("The camera ID was not detected.")
        else:
            print("Input is invalid.")

    while True:
        print("(2) Input [exclude ID] or [100]")
        input_key=input()
        if int_check(input_key):
            input_int=int(input_key)
            if captures_ID.count(input_int):
                captures_ID.remove(input_int)
                print(captures_ID)
            elif input_int==100:
                break
            else:
                print("The camera ID was not detected.")
        else:
            print("Input is invalid.")
    print("------------------")


def int_check(check_num):
    try:
        int(check_num)
    except ValueError:
        return False
    else:
        return True

def wait_setting():
    while True: 
        f = open('waiting.txt', 'r')
        data = f.read()
        f.close()
        if(data=='OK'):
            break
        time.sleep(0.1) # waiting

def UDP_initial():
    global local_address, multicast_group, port, bufsize, sock

    # $ipconfig/all or $ifconfig
    local_address   = '100.64.1.32'
    multicast_group = '239.255.0.1'
    port = 4000
    bufsize = 4096

    sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))
    sock.setsockopt(socket.IPPROTO_IP,
                    socket.IP_ADD_MEMBERSHIP,
                    socket.inet_aton(multicast_group) + socket.inet_aton(local_address))

    '''
    with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', port))
        sock.setsockopt(socket.IPPROTO_IP,
                        socket.IP_ADD_MEMBERSHIP,
                        socket.inet_aton(multicast_group) + socket.inet_aton(local_address))
    '''


def UDP_receive(command, comment):
    while True:
        try:
            print("IN")
            data=sock.recv(bufsize)
            print("recv data: " + data.decode())
        except:
            pass
        else:
            if data.decode() == command:
                print(comment)
            break
    return data.decode()


if __name__ == '__main__':
   main_multithread()