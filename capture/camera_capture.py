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
    make_directory("./capture")

    cap = cv2.VideoCapture(1)
    camera_setting(cap)
    camera_setting_show(cap)

    print(" ")
    print('capture = c, exit = esc')

    n = 0
    height_fix=540
    while True:
        ret, frame = cap.read()
        width=frame.shape[1]
        height=frame.shape[0]
        rate=height_fix/float(height)
        resized_frame = cv2.resize(frame,(int(width*rate), int(height*rate)))
        cv2.imshow('framename', resized_frame)

        key = cv2.waitKey(10)
        if key == ord('c'):
            cv2.imwrite('{}_{}.{}'.format('capture/capture', n, 'jpg'), frame)
            n += 1
        elif key == 27:
            break
    cap.release()
    cv2.destroyWindow('framename')


def check_camera():
    height_fix=540
    while True:
        print("check: input [camera ID] or [esc]")
        input_key=input()
        if input_key=='esc':
            print("break")
            break
        if int_check(input_key):
            input_int=int(input_key)
            capture = cv2.VideoCapture(input_int) #cv2.CAP_DSHOW
            if capture.isOpened():
                camera_setting(capture)
                camera_setting_show(capture)
                print("set up camera ID: " + str(input_int))
                print("exit: frame windows -> esc")
                while True:
                    ret, frame = capture.read()
                    width=frame.shape[1]
                    height=frame.shape[0]
                    rate=height_fix/float(height)
                    resized_frame = cv2.resize(frame,(int(width*rate), int(height*rate)))
                    cv2.imshow("Camera ID: " + str(input_key), resized_frame)
                    key = cv2.waitKey(10)
                    if key == 27: # esc
                        break
                capture.release()
                cv2.destroyWindow("Camera ID: " + str(input_key))
                print("release camera ID: " + str(input_int))
            else:
                print("Input is invalid.")
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

def make_directory(dir):
    print("create a directory, " + str(dir))
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)