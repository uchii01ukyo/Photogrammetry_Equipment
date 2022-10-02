import cv2
 
camera = cv2.VideoCapture(0)
 
# Save setting
fps = int(camera.get(cv2.CAP_PROP_FPS))
w = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')        # fourcc - mp4
video = cv2.VideoWriter('video.mp4', fourcc, fps, (w, h))  # filename, fourcc, fps, size
 
# Capture
while True:
    ret, frame = camera.read()
    cv2.imshow('camera', frame)
    video.write(frame)
 
    # esp
    if cv2.waitKey(10) == 27:
        break
 
camera.release()
cv2.destroyAllWindows()