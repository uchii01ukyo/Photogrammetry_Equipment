# coding: UTF-8
import cv2
import os
import time
import threading
import keyboard
import socket

captures_ID = []

def main_multithread():

    # UDP
    UDP_initial()
    received=UDP_receive('open')
    
    # make main directory
    dir = "./capture"
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    # camera detection
    detection()

    # initial
    time_start=time.time()
    thread=[0]*(len(captures_ID)+1)
    captures=[0]*(len(captures_ID)+1)
    # clear text
    f = open("waiting.txt","w")
    f.close()

    # main-connection
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
    
    print("---> capture = c, exit = esc")
    while True:
        received=UDP_receive('c')
        f = open('waiting.txt', 'w')
        f.write(received)
        if received == "esc":
            break
        time.sleep(1)
        f = open('waiting.txt', 'w')
        f.close()

    
    for ID in captures_ID:
        thread[ID].join()
    
    print("All completed successfully!")


def camera_capture(ID, captures, time_start):
    
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

    n=0
    while True: 
        f = open('waiting.txt', 'r')
        data = f.read()
        f.close()
        if data=='c':
            ret, frame = captures[ID].read()
            cv2.imwrite('{}_{}_{}.{}'.format('camera', ID, n, 'jpg'), frame)
            time_now=time.time()-time_start
            print("ID: " + str(ID) + "-> capture (" + str(time_now) + " sec)")
            n += 1
            time.sleep(2)
        elif data == 'esc':
            break
    captures[ID].release()


def detection():
    ID=1
    print("---detection---")
    while True:
        capture = cv2.VideoCapture(ID,cv2.CAP_DSHOW)
        if capture.isOpened():
            print("ID: " + str(ID) + " -> Found")
            captures_ID.append(ID)
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

def UDP_initial():
    global udpSock, Client_Addr, UDP_SERIAL_Addr, UDP_BUFSIZE

    # $ipconfig/all or $ifconfig
    Client_IP = "192.168.11.6"
    Client_Port = 50000
    Client_Addr = (Client_IP, Client_Port)
    UDP_SERIAL_IP = "192.168.11.8"
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
            print("NG")
            pass
        else:
            if data.decode() == command:
                print(comment)
                break
    return data.decode()


if __name__ == '__main__':
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