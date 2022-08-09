import requests
import base64
import os

url = "http://127.0.0.1:7579/Mobius"


def encode_img(filename):
    f = open(filename, "rb")
    fileContent = f.read()
    byteArr = bytearray(fileContent)
    imgbyte = base64.b64encode(byteArr)
    f.close()
    return imgbyte


def create_cnt():
	folder_path = "/home/yamewrong/Desktop/lab/dataAug/mobius-dataAug/test_script/CSE-filesystem"
	folder_list = os.listdir(folder_path)
	image_list = [file for file in folder_list if file.endswith(".jpg")]
	print ("image_list: {}".format(image_list))
	print("Input Image")
	global select_name
	select_name = input()
	cnt = 1
	for file in image_list:
		if(file==select_name):
			cnt = 0
	if cnt==1:
		print("Invalid Input")
		return 0
	filename = "/home/yamewrong/Desktop/lab/dataAug/mobius-dataAug/test_script/CSE-filesystem/"+select_name          
	payload = {
		"m2m:cin": {
		"rn": select_name,
		"con": encode_img(filename)
        }
    }

	headers = {
        'Accept': 'application/json',
        'X-M2M-RI': '12345',
        'X-M2M-Origin': 'SvirtualStore',
        'Content-Type': 'application/vnd.onem2m-res+json; ty=4'
    }

	response = requests.post(url + '/virtualStore/classifier/target', json=payload, headers=headers)
	print(response.json())


create_cnt()

