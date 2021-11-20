import requests
import json
import base64


def getByte(path):
    with open(path, 'rb') as f:
        img_byte = base64.b64encode(f.read())
    img_str = img_byte.decode('ascii')
    return img_str


img_str = getByte('hah.jpg')
url = 'http://43.129.251.135:80/upload'
data = {'picture': [{"filename": "hah.jpg", "content": img_str}]}
json_mod = json.dumps(data)
res = requests.post(url=url, data=json_mod)
