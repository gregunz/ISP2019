import json
import requests

data_json_shipping = {
    'shipping_address': 'gregoire.clement@epfl.ch', 
    'product': 'sHa+M4HUY8IBVVMc3YE+YGC8oWaveWGDOtjoV72m258='
}
r = requests.post("http://com402.epfl.ch/hw1/ex3/shipping", json=data_json_shipping)
print(r)
print(r.content)

data_json_sensitive = {
    'student_email': 'gregoire.clement@epfl.ch', 
    'secrets': ['0014/6066/5888/0929', '5114.9164.5954.0250', 'R8JA6056?W6N@', '2602/1606/8751/0755', '8UY;29YO:66YRA']
}
r = requests.post("http://com402.epfl.ch/hw1/ex4/sensitive", json=data_json_sensitive)
print(r)
print(r.content)

