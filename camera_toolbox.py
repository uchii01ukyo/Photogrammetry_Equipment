import cv2
import datetime

CameraID=1

def camera_detection():
        
    print('[', datetime.datetime.now(), ']', 'searching any camera...')

    true_camera_is = []

    for i1 in range(0, 20): 
        cap = cv2.VideoCapture(i1)
        ret, frame = cap.read()

        if ret is True:
            true_camera_is.append(i1)
            print("camera_number", i1, "Find!")
        else:
            print("camera_number", i1, "None")

        cap.release() 

    print("Result: ", len(true_camera_is))


def get_camera_propaties():
    params = ['MSEC',
            'POS_FRAMES',
            'POS_AVI_RATIO',
            'FRAME_WIDTH',
            'FRAME_HEIGHT',
            'PROP_FPS',
            'PROP_FOURCC',
            'FRAME_COUNT',
            'FORMAT',
            'MODE',
            'BRIGHTNESS',
            'CONTRAST',
            'SATURATION',
            'HUE',
            'GAIN',
            'EXPOSURE',
            'CONVERT_RGB',
            'WHITE_BALANCE',
            'RECTIFICATION']

    cap = cv2.VideoCapture(CameraID)
    for num in range(19):
        print(params[num], ':', cap.get(num))

