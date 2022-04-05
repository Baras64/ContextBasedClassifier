import requests
import json
URL = 'http://127.0.0.1:5000/api/V4CWUCG/if else then Sachin'
res = requests.get(URL)
resjson = json.loads(res.text)
print(resjson['predicted_text'])

