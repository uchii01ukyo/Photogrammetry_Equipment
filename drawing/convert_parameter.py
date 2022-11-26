import cv2
import numpy as np
import os
import shutil

def main():
    make_directory('./output')

    #directory = '../capture/capture'
    directory='/Users/uchiiukyo/Desktop/capture/capture2_0'
    print(sum(os.path.isfile(os.path.join(directory,name)) for name in os.listdir(directory)))

    ID=0
    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        if os.path.isfile(file) and filename.endswith('.jpg'):
            print(file)
            convert(file,1.8,0,ID)
            ID=ID+1

def convert(picture,alpha,beta,ID):
    src = cv2.imread(picture)
    dst = adjust(src, alpha,beta)
    cv2.imwrite('output/output' + str(ID) + '.jpg' ,dst)

def adjust(img, alpha, beta):
    dst = alpha * img + beta
    return np.clip(dst, 0, 255).astype(np.uint8)

def make_directory(dir):
    print("create a directory, " + str(dir))
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)

if __name__ == '__main__':
   main()
