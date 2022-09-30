# coding: UTF-8
import cv2
import os
import time


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
            print("VideoCapture(" + str(ID) + ") -> Found")
            ID += 1

    # camera_detection()
    print('-> Prepare OK')
    
    n=0
    while True:
        start = time.time()
        n+=1
        print('capture ' + str(n))

        # make sub directory
        sub_dir="./" + dir + "/" + str(n)
        if not os.path.exists(sub_dir):
            os.makedirs(sub_dir)

        # capture
        print('Here')
        for ID, capture in enumerate(captures):
            print('IN')
            ret, frame = capture.read()
            path=sub_dir + "/camera"
            cv2.imwrite('{}_{}.{}'.format(path, ID, 'jpg'), frame)
            print(ID + ' -> OK')

        print(time.time() - start)
        time.sleep(5)

    capture.release()
    
"""
n = 0
while True:
    ret, frame = cap.read()

    height = frame.shape[0]
    width = frame.shape[1]
    resized_frame = cv2.resize(frame,(width/2, height/2))

    cv2.imshow('framename', resized_frame)

    key = cv2.waitKey(10)
    if key == ord('c'):
        cv2.imwrite('{}_{}.{}'.format('camera_capture', n, 'jpg'), frame)
        n += 1
    elif key == 27:
        break

cap.release()
cv2.destroyWindow('framename')
"""

def capture(i,sub_dir):
    cap = cv2.VideoCapture(i)
    ret, frame = cap.read()
    path=sub_dir + "/camera"
    cv2.imwrite('{}_{}.{}'.format(path, i, 'jpg'), frame)
    cap.release()


def camera_detection():
    print("-- Connect Camera --")
    ID=0
    while True:
        cap1 = cv2.VideoCapture(ID)
        if cap1.isOpened(): 
            print("VideoCapture(" + str(ID) + ") -> Found")
            cap1.release() 
            ID+=1
        else:
            break
    if(ID<=1):
        print("Error: Not connecting camera")
        exit()
    else:
        print("----")


if __name__ == '__main__':
    main()