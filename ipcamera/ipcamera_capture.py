import cv2

user_id = "admin" 
user_pw = "password" 
host = "192.168.0.1" 
cap = cv2.VideoCapture(f"rtsp://{user_id}:{user_pw}@{host}/MediaInput/h264")

while(True):
    try:
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow('VIDEO', frame)
        cv2.waitKey(1)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        break

cap.release()
cv2.destroyAllWindows()