#%%
import websockets
import asyncio
import binascii
from hashlib import sha256
import random
import string
#%%
def encode(i):
    if type(i) is int:
        buf = i.to_bytes((i.bit_length() + 7) // 8, 'big')
        return binascii.hexlify(buf).decode('utf-8')
    else:
        return i.encode('utf-8')

#%%
def decode(s):
    buf = binascii.unhexlify(s)
    return int.from_bytes(buf, 'big')
#%%
def rand_hex(n=32):
    random.seed(238122)
    ls = [random.choice(string.hexdigits) for n in range(n)]
    return "".join(ls)
#%%
ws_url = 'ws://com402.epfl.ch/hw2/ws'
H = lambda x: sha256(x if type(x) is bytes else binascii.unhexlify(x)).hexdigest()
N_hex="""EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9E\
A2314C9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E\
250B98BE48E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B\
15D4982559B297BCF1885C529F566660E57EC68EDBC3C05726CC0\
2FD4CBF4976EAA9AFD5138FE8376435B9FC61D2FC0EB06E3"""
N = decode(N_hex)
g = 2
k_hex = H(N_hex + encode(g))
print(f'N = {N}')
print(f'g = {g}')

U = "gregoire.clement@epfl.ch"
password = 'KRcTAh1JAQBAB0wETQ0bGSELUBIDDgcH'
print(f'U = {U}')
print(f'password = {password}')

#%%
async def hello():
    async with websockets.connect(ws_url) as websocket:

        await websocket.send(encode(U))
        print(f"> U = {encode(U)}")

        salt_hex = await websocket.recv()
        print(f"< salt_hex = {salt_hex}")
        salt = decode(salt_hex)

        a = decode(rand_hex(32))
        print(f'a = {a}')
        A = pow(g, a, N)
        A_hex = encode(A)
        await websocket.send(A_hex)
        print(f'> A_hex = {A_hex}')

        B_hex = await websocket.recv()
        B = decode(B_hex)
        print(f"< B_hex = {B_hex}")

        u_hex = H(A_hex + B_hex)
        u = decode(u_hex)
        x_hex = H(salt_hex + H((U + ':' + password).encode()))
        x = decode(x_hex)
        print(f'x = {x}')
        S = pow(B - pow(g, x, N), a + u * x, N)
        print(f'S = {S}')
        S_hex = encode(S)
        token_req = H(A_hex + B_hex + S_hex)
        await websocket.send(token_req)
        print(f'> token_req = {token_req}')
        
        token_enc = await websocket.recv()
        print(f'< token = {token_enc}')

asyncio.get_event_loop().run_until_complete(hello())
#%%

#%%
