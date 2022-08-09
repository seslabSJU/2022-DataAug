import requests

url = "http://127.0.0.1:7579/Mobius"

def create_classifier(): 
	payload = {
		"m2m:cnt": {
	  		"rn": "classifier",
			"lbl": ["classifier"],
			"mbs": 999999
		}
	}
	headers = {
	  'Accept': 'application/json',
	  'X-M2M-RI': '12345',
	  'X-M2M-Origin': 'SvirtualStore',
	  'Content-Type': 'application/vnd.onem2m-res+json; ty=3'
	}
	
	response = requests.post(url+'/virtualStore', json=payload, headers=headers)
	print(response.text)
	
create_classifier()

