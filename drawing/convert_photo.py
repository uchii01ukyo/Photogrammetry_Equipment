import cv2
import os
import shutil
import math

def main():
    make_directory('./picture')

    #directory = '../capture/capture'
    directory='/Users/uchiiukyo/Desktop/photogrammetry_data/capture4'
    ID=0
    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        if os.path.isfile(file) and filename.endswith('.mp4'):
            print(file)
            save_frame_range(file, 55.8, 56.8, ID)
            ID=ID+1


def save_frame_range(video_dir, start_sec, stop_sec, ID):

    cap = cv2.VideoCapture(video_dir)
    if not cap.isOpened():
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    print(" - FPS: " + str(round(fps)))

    start_frame=int(math.floor(start_sec*fps))
    stop_frame=int(math.ceil(stop_sec*fps))
    print(" - Frame number: " + str(start_frame) + "-" + str(stop_frame))

    for n in range(start_frame, stop_frame):
        cap.set(cv2.CAP_PROP_POS_FRAMES, n)
        ret, frame = cap.read()
        frame_sec='{:.02f}'.format(n/fps)
        if ret:
            cv2.imwrite('{}_{}_{}sec.{}'.format('picture/picutre', ID, frame_sec, 'jpg'), frame)
        else:
            return

    cap.set(cv2.CAP_PROP_POS_FRAMES, round(fps * start_sec))
    ret, frame = cap.read()


def make_directory(dir):
    print("create a directory, " + str(dir))
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)

                 
if __name__ == '__main__':
   main()
  