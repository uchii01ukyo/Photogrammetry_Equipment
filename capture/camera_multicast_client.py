# coding: UTF-8
from __future__ import print_function
import cv2
import os
import time
import threading
import socket
import shutil
from contextlib import closing
import sys

captures_ID = []


def main():
    initial_setting()

    # UDP
    UDP_initial()
    print("wait... start up the command on the server device!")
    received=UDP_receive('open','opened')
    
    # make main directory
    make_directory("./capture")
    print(" ")

    # camera detection
    print("--- 1. Detection ---")
    detection()

    # camera selection
    # print("----- 2. Selection ------")
    # selection()

    # initial
    global time_start, thread, captures, connect_num, camera_num
    time_start=time.time()
    thread=[0]*(len(captures_ID)+1)
    captures=[0]*(len(captures_ID)+1)
    camera_num=len(captures_ID)
    connect_num=0
    # clear text
    f = open("waiting.txt","w")
    f.close()


    print("--- 3. connection ---")
    print("Connecting ... " + str(camera_num))

    # mode
    if(MODE=='movie'):
        mode_movie()
    elif(MODE=='picture'):
        mode_picture()
    else:
        print('invalid mode! select mode, picture / movie.')

    # multithread join
    for ID in captures_ID:
        thread[ID].join()
    
    print(" ")
    print("All completed successfully!")


def initial_setting():
    global FILE_NAME, MODE, FRAME_WIDTH, FRAME_HEIGHT, FRAME_FPS, FRAME_BRIGHT

    args = sys.argv
    if(args[0]=='picture') or (args[0]=='movie'):
        print('invaid input mode value! input only picture/movie.')
        sys.exit()

    for num in range(2,6):
        if(int_check(args[num])==False):
            print('invaid input value! input only [int].')
            sys.exit()

    FILE_NAME=args[0]
    MODE=args[1]
    FRAME_WIDTH=args[2]
    FRAME_HEIGHT=args[3]
    FRAME_FPS=args[4]
    FRAME_BRIGHT=args[5]

    print(' ')
    print(str(FILE_NAME))
    print('- MODE         : ' + str(MODE))
    print('- FRAME_WIDTH  : ' + str(FRAME_WIDTH ))
    print('- FRAME_HEIGHT : ' + str(FRAME_HEIGHT))
    print('- FRAME_FPS    : ' + str(FRAME_FPS))
    print('- FRAME_BRIGHT : ' + str(FRAME_BRIGHT))
    print(' ')


def camera_connect_waiting():
    while True: 
        global connect_num, camera_num
        if connect_num==camera_num:
            f = open('waiting.txt', 'w')
            f.write('OK')
            f.close()
            break
        time.sleep(0.1)
    print("-------------------")
    print("All connected.")


def set_multithread(target):
    lock = threading.RLock()
    for ID in captures_ID:
        th=threading.Thread(target=target, name="camera" + str(ID), args=(ID,captures,lock))
        thread[ID]=th
        thread[ID].start()


def mode_movie():
    set_multithread(camera_capture_movie)
    camera_connect_waiting()
    print(" ")

    while True:
        received=UDP_receive('c','[ capture start ]')
        f = open('waiting.txt', 'w')
        f.write(received)
        f.close()
        print("UDP received -> " + received)
        if received == "esc":
            print(" [ exit ]")
            break


def mode_picture():
    set_multithread(camera_capture_picture)
    camera_connect_waiting()
    print(" ")

    while True:
        received=UDP_receive('c','[ capture ]')
        f = open('waiting.txt', 'w')
        f.write(received)
        f.close()
        print("UDP received -> " + received)
        if received == "esc":
            print(" [ esc ]")
            break
        # clear
        time.sleep(1)
        received=""
        f = open('waiting.txt', 'w')
        f.write(received)
        f.close()


def camera_setting(cap):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(FRAME_WIDTH))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(FRAME_HEIGHT))
    cap.set(cv2.CAP_PROP_FPS, int(FRAME_FPS))
    cap.set(cv2.CAP_PROP_BRIGHTNESS, int(FRAME_BRIGHT))
    #camera_setting_show(cap)
 

def camera_setting_show(cap):
    print(" ")
    print("FRAME_WIDTH  : " + str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print("FRAME_HEIGHT : " + str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("FPS          : " + str(cap.get(cv2.CAP_PROP_FPS)))
    print("BRIGHTNESS   : " + str(cap.get(cv2.CAP_PROP_BRIGHTNESS)))
    print("CONTRAST     : " + str(cap.get(cv2.CAP_PROP_CONTRAST)))
    print("SATURATION   : " + str(cap.get(cv2.CAP_PROP_SATURATION)))
    print("HUE          : " + str(cap.get(cv2.CAP_PROP_HUE)))
    print("GAIN         : " + str(cap.get(cv2.CAP_PROP_GAIN)))
    print("EXPOSURE     : " + str(cap.get(cv2.CAP_PROP_EXPOSURE)))
    print(" ")


def camera_capture_movie(ID, captures, lock):
    
    # connect
    captures[ID] = cv2.VideoCapture(ID) #(ID,cv2.CAP_DSHOW) 
    if captures[ID].isOpened():
        with lock:
            print("ID: " + str(ID) + " -> Connected")
            global connect_num
            connect_num=connect_num+1
    else:
        with lock:
            print("ID: " + str(ID) + " -> Failed")

    # camera setting
    camera_setting(captures[ID])

    # mp4 setting
    fps = int(captures[ID].get(cv2.CAP_PROP_FPS))
    w = int(captures[ID].get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(captures[ID].get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')        # fourcc - mp4
    video = cv2.VideoWriter('capture/video_' + str(ID) + '.mp4', fourcc, fps, (w, h))  # filename, fourcc, fps, size

    # wait
    wait_setting()

    # wait
    while True: 
        f = open('waiting.txt', 'r')
        data = f.read()
        f.close()
        if data=='c':
            time.sleep(0.005*ID)
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


def camera_capture_picture(ID, captures, lock):

    # connect
    captures[ID] = cv2.VideoCapture(ID) #(ID,cv2.CAP_DSHOW) 
    if captures[ID].isOpened():
        with lock:
            print("ID: " + str(ID) + " -> Connected")
            global connect_num
            connect_num=connect_num+1
    else:
        with lock:
            print("ID: " + str(ID) + " -> Failed")

    # camera setting
    camera_setting(captures[ID])

    # wait
    wait_setting()

    # capture
    n=0
    while True: 
        f = open('waiting.txt', 'r')
        data = f.read()
        f.close()
        if data=='c':
            time.sleep(0.005*ID)
            ret, frame = captures[ID].read()
            cv2.imwrite('{}_{}_{}.{}'.format('capture/camera', ID+40, n, 'jpg'), frame)
            print("ID: " + str(ID) + "-> capture")
            n += 1
            time.sleep(1)
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


def UDP_initial():
    global local_address, multicast_group, port, bufsize, sock

    local_address_ex = socket.gethostbyname_ex(socket.gethostname())
    local_adress_list=local_address_ex[2]
    local_address=local_adress_list[-1]
    print("UDP setting")
    print("- IPv4_address      : " + str(local_address))
    
    multicast_group = '239.255.0.1'
    port = 4000
    bufsize = 4096
    print("- multicast_address : " + str(multicast_group))
    print(" ")

    sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))
    sock.setsockopt(socket.IPPROTO_IP,
                    socket.IP_ADD_MEMBERSHIP,
                    socket.inet_aton(multicast_group) + socket.inet_aton(local_address))


def UDP_receive(command, comment):
    while True:
        try:
            print('UDP waiting...')
            data=sock.recv(bufsize)
            print("receive data: " + data.decode())
        except:
            pass
        else:
            if data.decode() == command:
                print(comment)
            break
    return data.decode()


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