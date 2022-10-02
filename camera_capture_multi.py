# coding: UTF-8
import cv2
import os
import time
import threading

# simple
def main():

    # make main directory
    dir = "./capture"
    if not os.path.exists(dir):
        os.makedirs(dir)

    ID=0
    flag = True
    captures = []
    while( flag ):
        capture = cv2.VideoCapture(ID)
        ret, frame = capture.read()
        flag = ret
        if flag:
            captures.append(capture)
            print("VideoCapture(" + str(ID) + ") -> Found")
            ID += 1

    # camera_detection()
    print('-> Prepare OK')
    
    n=0
    while True:
        key = cv2.waitKey(10)

        if key == ord('c'):
            n+=1
            print('capture ' + str(n))

            # make sub directory
            sub_dir="./" + dir + "/" + str(n)
            if not os.path.exists(sub_dir):
                os.makedirs(sub_dir)

            # capture
            for ID, capture in enumerate(captures):
                ret, frame = capture.read()
                path=sub_dir + "/camera"
                cv2.imwrite('{}_{}.{}'.format(path, ID, 'jpg'), frame)
                print(ID + ' -> OK')

        elif key == 27:
            break

    capture.release()
    

def main_multithread():
    # make main directory
    dir = "./capture"
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    ID=0
    flag = True
    captures = []
    while( flag ):
        capture = cv2.VideoCapture(ID)
        ret, frame = capture.read()
        flag = ret
        if flag:
            captures.append(capture)
            print("VideoCapture(" + str(ID) + ") -> Found")
            ID += 1
    
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

def camera_capture(ID):
    cap = cv2.VideoCapture(ID)
    n = ID*10
    while True:
        key = cv2.waitKey(1)
        if key == ord('c'):
            ret, frame = cap.read()
            cv2.imwrite('{}_{}.{}'.format('camera_capture', n, 'jpg'), frame)
            n += 1
        elif key == 27:
            break
    cap.release()


if __name__ == '__main__':
    main()
    #main_multithread()