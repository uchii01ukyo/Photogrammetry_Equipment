import threading
import time
import sys


def target(ID, lock):
    with lock:
        time.sleep(1)
        global num
        num=num+1
        print(num)
        #print(str(ID) + ": OK")


def main():
    #for ID in range(10):
    #    print(str(ID) + ": ")

    thread=[0]*10
    lock = threading.RLock()
    global num
    num=0
    for ID in range(10):
        th=threading.Thread(target=target, args=(ID,lock,))
        thread[ID]=th
        thread[ID].start()

    for ID in range(10):
        thread[ID].join()

if __name__ == '__main__':
   main()