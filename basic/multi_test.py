# coding: UTF-8
import cv2
import keyboard
import os
import time
import threading
import multiprocessing

# How to use multithread
def main_multithread():
    time_start=time.time()
    print("start")
    t1 = threading.Thread(target=camera_capture, name="camera1", args=(1,time_start,))
    t2 = threading.Thread(target=camera_capture, name="camera2", args=(2,time_start,))
    t3 = threading.Thread(target=camera_capture, name="camera3", args=(3,time_start,))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    print("end")

# How to use multithread
def main_multithread_loop():
    print("start")
    time_start=time.time()
    thread=[]
    loop_times=20
    for num in range(loop_times):
        thread.append(threading.Thread(target=camera_capture, name="camera" + str(num), args=(num,time_start,)))
        thread[num].start()
    for num in range(loop_times):
        thread[num].join()
    print("end")

# How to use multiprocess
def main_multiprocess():
    time_start=time.time()
    print("start")
    p1 = multiprocessing.Process(target=camera_capture, args=(1,time_start,))
    p2 = multiprocessing.Process(target=camera_capture, args=(2,time_start,))
    p3 = multiprocessing.Process(target=camera_capture, args=(3,time_start,))
    p1.start()
    p2.start()
    p3.start()


def camera_capture(ID, time_start):
    n = 0
    while True:
        if keyboard.read_key() == "c":
            time_now=time.time()-time_start
            print("ID:" + str(ID) + "-> " + str(time_now) + " sec")
            time.sleep(2)
        elif keyboard.read_key() == "esc":
            break

if __name__ == '__main__':
    main_multithread_loop()