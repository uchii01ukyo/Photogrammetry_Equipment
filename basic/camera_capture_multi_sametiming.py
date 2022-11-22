# coding: UTF-8
import cv2
import os
import time
import threading
import keyboard

captures_ID = []
a=0

def main_multithread():

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

    print("---capture = c, exit = esc---")
    
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
        if keyboard.read_key() == "c":
            ret, frame = captures[ID].read()
            cv2.imwrite('{}_{}_{}.{}'.format('camera', ID, n, 'jpg'), frame)
            time_now=time.time()-time_start
            print("ID: " + str(ID) + "-> capture (" + str(time_now) + " sec)")
            n += 1
            time.sleep(2)
        elif keyboard.read_key() == "esc":
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