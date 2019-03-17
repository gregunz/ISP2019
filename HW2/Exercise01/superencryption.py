#%%
import base64

def superencryption(msg,key):
    if len(key) < len(msg):
        diff = len(msg) - len(key)
        key += key[:diff]
    amsg = [ord(c) for c in msg]
    akey = [ord(c) for c in key[:len(amsg)]]
    assert len(amsg) == len(akey)

    s = [chr(m ^ akey[i]) for i, m in enumerate(amsg)]
    s = ''.join(s).encode('ascii')
    return base64.b64encode(s).decode('utf-8')

#%%
mySecureOneTimePad = "Never send a human to do a machine's job"
'KRcTAh1JAQBAB0wETQ0bGSELUBIDDgcH' == superencryption("gregoire.clement@epfl.ch", mySecureOneTimePad)

#%%
