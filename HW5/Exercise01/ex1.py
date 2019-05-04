import numpy as np
import bitarray
from scipy.io import wavfile

fname = '../../data/audio.wav'

def decoder(bit_array):
    try:
        if type(bit_array) is np.ndarray and len(bit_array.shape) == 1:
            bit_array = bit_array.tolist()
        return bitarray.bitarray(bit_array).tobytes().decode()
    except:
        return ''
    
fs, data = wavfile.read(fname)

from_ = 5000000 #found previously using np.argmax((data >> 0 & 1)[:, 1]) which is the first one
to_ = from_ + 208

lsb = (data >> 0 & 1)[from_:to_]

token = decoder(lsb.flatten())

#print(token)
print('ex1 = "{}"'.format(token[7:-1]))