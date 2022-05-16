# import requests
#
# # endpoint = "http://localhost:8000/thumbnails/"
# endpoint = "http://localhost:8000/images/"
#
# data = {
#     'user': 5,
#     'size': 200,
# }
#
# files = {
#     'image': (open('/home/mg/Pictures/paragon.jpg'), 'multipart/form-data', {'Expires': '0'})
# }
#
# headers = {
#     'content-type': 'multipart/form-data'
# }
#
# # response = requests.get(url=endpoint)
# response = requests.post(url=endpoint, json=data, files=files)
# print(response.json())

import hashlib
import pickle
import zlib

from cryptography.fernet import Fernet
from datetime import datetime
key = Fernet.generate_key()
current_time = datetime.now().strftime("%H-%M-%S")
print(current_time)
# text = zlib.compress(pickle.dumps("data", 0)).encode('base64')
f = Fernet(b'OGO8gP9HLbbJeEyt-_NgqM3Mmi4t-cUtomvC3w4MJYc=')
token = f.encrypt("b" + "'" + current_time + "'")
print(token)
print(f.decrypt(token))

# token = f.encrypt_at_time(b'30', current_time)
# print(token)
