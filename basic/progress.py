from time import sleep
import random
from tqdm import tqdm
from multiprocessing import Pool, freeze_support, RLock
from contextlib import closing
import threading

L = 8


def long_time_process(p):
    info = str(p)
    for i in tqdm(range(20), desc=info, position=p+1):
        sleep(random.random())
    return p


if __name__ == '__main__':
    '''
    #freeze_support()
    with closing(Pool(L)) as p:
            #initializer=tqdm.set_lock, initargs=(RLock(),)) as p:
            result = p.map(long_time_process, range(L))
            print("\n" * L)
            print(result)
            p.terminate()
    '''

    th=threading.Thread(target=long_time_process, name=str(1), args=(1,))
    th2=threading.Thread(target=long_time_process, name=str(2), args=(2,))
    th.start()
    th2.start()
    th.join()
    th2.join()
