import threading
import time
import sys

def target(ID, lock):
    with lock:
        time.sleep(1)
        print("\033[" + str(10-ID+1) + "A")
        print(str(ID) + ": OK")
        print("\033[4A")
        print("\033[" + str(10-ID+1) + "B")


def main():
    for ID in range(10):
        print(str(ID) + ": ")

    thread=[0]*10
    lock = threading.RLock()
    for ID in range(10):
        th=threading.Thread(target=target, args=(ID,lock,))
        thread[ID]=th
        thread[ID].start()

    for ID in range(10):
        thread[ID].join()

if __name__ == '__main__':
   main()