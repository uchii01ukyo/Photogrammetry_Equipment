from time import sleep
import random
from tqdm import tqdm
from multiprocessing import Pool, freeze_support, RLock
from contextlib import closing

L = 8


def long_time_process(p):
    info = str(p)
    for _ in tqdm(range(20), desc=info, position=p+1):
        sleep(random.random())
    return p * 2


if __name__ == '__main__':
    #freeze_support()
    with closing(Pool(2)) as p:
            #initializer=tqdm.set_lock, initargs=(RLock(),)) as p:
            result = p.map(long_time_process, range(L))
            print("\n" * L)
            print(result)
            p.terminate()