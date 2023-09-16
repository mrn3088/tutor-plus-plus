import requests
import json
import hashlib
import time


endpoint_name = "cpm-bee-230915034844EVUY"
ak = "21580531531411eeb4eb0242ac120004"
sk = "naj4HJrZZe7V5pKL4g#x#AJ-QEzOTOxO"
host = "saas-1222385307.us-west-2.elb.amazonaws.com"

timestemp = str(int(time.time()))
hl = hashlib.md5()
hl.update(f"{timestemp}{sk}".encode(encoding='utf-8'))
sign = hl.hexdigest()

url = f"http://{host}/inference"

def model_inference(input):
    payload = {
   "endpoint_name": endpoint_name,
   "input": json.dumps(input),
   "ak": ak,
   "timestamp": timestemp,
   "sign": sign
    }
    
    response = requests.post(url=url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    if response.status_code != 200:
        print(response.reason, response.text)
    else:
        obj_json = response.json()
    if obj_json['code'] != 0:
        print(obj_json)
    else:
        data_str = obj_json['data']['data']
        data_obj = json.loads(data_str)
        # print(data_obj)
        return data_obj['<ans>']
        

    