import cv2

for i1 in range(0, 20): 
    cap1 = cv2.VideoCapture(i1) #, cv2.CAP_DSHOW
    if cap1.isOpened(): 
        print("- VideoCapture(" + str(i1) + ") -> Found")
    else:
        print("- VideoCapture(" + str(i1) + ") -> None")
    cap1.release() 