# coding: UTF-8
import cv2
import keyboard
import os
import time
import threading
import multiprocessing


def main():
    print("start")
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

def main_multiprocess():
    print("start")
    p1 = multiprocessing.Process(target=camera_capture, args=(1,))
    p2 = multiprocessing.Process(target=camera_capture, args=(2,))
    p3 = multiprocessing.Process(target=camera_capture, args=(3,))
    p1.start()
    p2.start()
    p3.start()

    """
    while True:
        key = cv2.waitKey(10)
        if key == 'c':
            print("IN")
        elif key == 27:
            break
    print("end")
    """

def camera_capture(ID):
    n = 0
    print(ID)
    while True:
        key = cv2.waitKey(10)
        if key == 'c':
            print("ID: " + ID + ", Times: " + n)
            n += 1
        elif key == 27:
            break

if __name__ == '__main__':
    main_multiprocess()