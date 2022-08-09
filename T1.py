import requests
import time
import os
url = "http://127.0.0.1:7579/Mobius"

def create_da():
	folder_path = "/home/yamewrong/Desktop/lab/dataAug/mobius-dataAug/test_script/CSE-filesystem"
	folder_list = os.listdir(folder_path)
	image_list = [file for file in folder_list if file.endswith(".jpg")]
	print ("image_list: {}".format(image_list))
	print("Input Image")
	global select_name
	select_name = input()
	print("Input rn")
	global rn
	rn = str(input())
	print("Input augty")
	print(" [ 'rotate' , ' cropping ' , ' flipping ' ] ")
	global augty
	augty = str(input())
	print("Input left [0~20]")
	global left
	left = int(input())
	print("Input right [0~20]")
	global right
	right = int(input())
	print("Input amount")
	global amount
	amount = int(input())
	print("Input label")
	global label
	label = str(input())

	payload = {
		"m2m:da": {
		"rn": rn,
            "augty": augty,
            "srsrc": "/virtualStore/classifier/target/"+select_name,
            "augprm": {
                "max_left_rotation": left,
                "max_right_rotation": right,
                "amount": amount,
                "label": label
            },
            "trgrsrc": "/virtualStore/classifier/target"+select_name
        }
    }
	headers = {
        'Accept': 'application/json',
        'X-M2M-RI': '12345',
        'X-M2M-Origin': 'SvirtualStore',
        'Content-Type': 'application/vnd.onem2m-res+json; ty=50'
    }
	response = requests.post(url + '/virtualStore', json=payload, headers=headers)
	print(response.text)


create_da()
