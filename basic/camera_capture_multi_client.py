# coding: UTF-8
import cv2
import os
import time
import threading
#import keyboard
import socket

captures_ID = []

def main_multithread():

    # UDP
    UDP_initial()
    print("wait when main device open")
    received=UDP_receive('open','opened')
    
    # make main directory
    dir = "./capture"
    if not os.path.exists(dir):
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
        # clear
        time.sleep(1)
        received=""
        f = open('waiting.txt', 'w')
        f.write(received)
        f.close()
        print("memo: " + received)

    
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

    f = open('waiting.txt', 'a')
    f.write(str(ID) + '\n')
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
    global udpSock, Client_Addr, UDP_SERIAL_Addr, UDP_BUFSIZE

    # $ipconfig/all or $ifconfig
    Client_IP = "100.64.1.32"#'172.23.3.97' #"192.168.11.6"
    Client_Port = 50000
    Client_Addr = (Client_IP, Client_Port)
    UDP_SERIAL_IP = "100.64.1.42"#"172.23.3.96"
    UDP_SERIAL_Port = 50000
    UDP_SERIAL_Addr = (UDP_SERIAL_IP, UDP_SERIAL_Port)
    UDP_BUFSIZE = 1024

    udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSock.bind(Client_Addr)
    udpSock.settimeout(1)
    

def UDP_send(command):
    print(command)
    udpSock.sendto(command.encode('utf-8'), UDP_SERIAL_Addr)

    while True:
        try:
            data, addr = udpSock.recvfrom(UDP_BUFSIZE)
        except:
            pass
        else:
            if data.decode() == 'ok':
                print("-> send OK")
                break


def UDP_receive(command, comment):
    while True:
        try:
            data, addr = udpSock.recvfrom(UDP_BUFSIZE)
        except:
            pass
        else:
            if data.decode() == command:
                print(comment)
                udpSock.sendto("ok".encode('utf-8'), addr)
                print("-> OK")
            break

    return data.decode()


if __name__ == '__main__':
   main_multithread()