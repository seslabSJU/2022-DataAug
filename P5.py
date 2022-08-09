import requests
import os

url = "http://127.0.0.1:7579/Mobius"

def make_cnt():
	folder_path = "/home/yamewrong/Desktop/lab/dataAug/mobius-dataAug/test_script/CSE-filesystem"
	folder_list = os.listdir(folder_path)
	image_list = [file for file in folder_list if file.endswith(".jpg")]
	for file in image_list:
		create_target(file)
		print("MAKE CNT",file)

def create_target(label):
	payload = {
		"m2m:cnt": {
	  		"rn": label,
			"lbl": [label],
			"mbs": 999999
		}
	}
	headers = {
	  'Accept': 'application/json',
	  'X-M2M-RI': '12345',
	  'X-M2M-Origin': 'SvirtualStore',
	  'Content-Type': 'application/vnd.onem2m-res+json; ty=3'
	}
	print("MAKE CNT OKAY",label)
	response = requests.post(url+'/virtualStore/classifier', json=payload, headers=headers)
	print(response.text)

make_cnt()
