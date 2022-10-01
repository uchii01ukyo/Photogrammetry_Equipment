import cv2
 
camera = cv2.VideoCapture(0)
 
# Save setting
fps = int(camera.get(cv2.CAP_PROP_FPS))                    # カメラのFPSを取得
w = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))              # カメラの横幅を取得
h = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))             # カメラの縦幅を取得
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')        # 動画保存時のfourcc設定（mp4用）
video = cv2.VideoWriter('video.mp4', fourcc, fps, (w, h))  # 動画の仕様（ファイル名、fourcc, FPS, サイズ）
 
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