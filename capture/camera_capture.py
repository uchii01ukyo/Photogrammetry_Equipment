# coding: UTF-8
import cv2
import os

FRAME_WIDTH=1920
FRAME_HEIGHT=1080
FPS=30
BRIGHTNESS=30
CONTRAST=34
SATURATION=64
HUE=0
GAIN=0
EXPOSURE=-6


def camera_capture():
    cap = cv2.VideoCapture(0)
    camera_setting(cap)
    camera_setting_show(cap)
    print('capture = c, exit = esc')

    n = 0
    while True:
        ret, frame = cap.read()
        resized_frame = cv2.resize(frame,(810, 540))
        cv2.imshow('framename', resized_frame)

        key = cv2.waitKey(10)
        if key == ord('c'):
            cv2.imwrite('{}_{}.{}'.format('camera_capture', n, 'jpg'), frame)
            n += 1
        elif key == 27:
            break
    cap.release()
    cv2.destroyWindow('framename')


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
                camera_setting(capture)
                camera_setting_show(capture)
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


def camera_setting(cap):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, BRIGHTNESS)
    cap.set(cv2.CAP_PROP_CONTRAST, CONTRAST)
    cap.set(cv2.CAP_PROP_SATURATION, SATURATION)
    cap.set(cv2.CAP_PROP_HUE, HUE)
    cap.set(cv2.CAP_PROP_GAIN, GAIN)
    cap.set(cv2.CAP_PROP_EXPOSURE, EXPOSURE)
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


def int_check(check_num):
    try:
        int(check_num)
    except ValueError:
        return False
    else:
        return True