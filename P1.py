import requests

url = "http://127.0.0.1:7579/Mobius"

def create_virtualStore():
	payload = {
		"m2m:ae": {
			'rn': 'virtualStore',
			"api": "0.2.481.2.0001.001.000111",
			"lbl": ["virtualStore"],
			"rr": True, 
		}
	}
	headers = {
	  'Accept': 'application/json',
	  'X-M2M-RI': '12345',
	  'X-M2M-Origin': 'SvirtualStore',
	  'Content-Type': 'application/json;ty=2'
	}
	response = requests.post(url, json=payload, headers=headers)
	print(response.text)
	
def sub_virtualStore_child():
	payload = {
		"m2m:sub":{
			"rn":"sub_da",
			"enc": {
				"net": [3]
			},
			"nu": [f"mqtt://localhost:7579/virtualStore/da?ct=json"],
		}
	}
	headers = {
	  'Accept': 'application/json',
	  'X-M2M-RI': '12345',
	  'X-M2M-Origin': 'SvirtualStore',
	  'Content-Type': 'application/vnd.onem2m-res+json; ty=23'
	}
	response = requests.post(url+'/virtualStore', json=payload, headers=headers)
	print(response.text)
	

create_virtualStore()
sub_virtualStore_child()
