import os
import binascii

import numpy as np
import pandas as pd
import itertools as it

from hashlib import sha256

from tqdm import tqdm_notebook as tqdm

H = lambda x: sha256(x.encode('utf-8') if type(x) is str else x).hexdigest()

sha1 = """efa52cf7077b052710cea2bdb5af38f16a1e99ac0bdc583fb2ae71ac675e8999
939d0e1ccf67d003fb03f23e34d406a9a8bc6692cb97fb5753cb7b25fd5de12f
3fca1d324e7142851d1ddf5c87bebd375e363094abac100ed20da75c6e5d6d9d
6b35f17b91f62b74a0b71c100fa349c5704cca921d3d2655f9d9795305ff3ab2
c921fba3ad7d1ab2b7ce7bf080755ff81540f36c1672aca046e663374331100f
94886ed84ed5bb5c8c050c12a76a5e12f75ce9d9886805cb80c6d6964401a21c
606b491415dbc766f3f165a329706494ed9e9848026be3aae026f8a8ca70a6bd
1b0de068c81afe94cda5e28fe6b65156477f24aa489b4e60ec93a6ae4d1dfbb9
570fcafd562921a52dd7897b633102342a0c55d51aff2b05f9efa4f15ce3e66e
0c1a7007a670aca720843c70395ebc7e8d54d84aa38e453ef104e6f69a026216""".split('\n')

found = dict()

chars = [chr(ord('a') + i) for i in range(26)] + [str(i) for i in range(10)]

import multiprocessing
from multiprocessing import Pool


num_cores = multiprocessing.cpu_count()
num_cores

passwords_1 = iter(''.join(c) for n in range(4, 7) for c in it.product(chars, repeat=n))

def process(p):
    if len(sha1) > len(found):
        h = H(p)
        if h in sha1:
            found[h] = p
            print(h, p)
            
with Pool(processes=num_cores) as pool:  # assuming Python 3
    pool.starmap(process, passwords_1)
    
    
print(found)