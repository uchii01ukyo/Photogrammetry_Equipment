#%!pip install tqdm
import tqdm
import numpy as np

for i in tqdm.tqdm(range(int(1e7))):
    np.pi*np.pi
