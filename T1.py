import requests
import time
import os
url = "http://127.0.0.1:7579/Mobius"

def create_da():
	folder_path = "/home/yamewrong/Desktop/lab/dataAug/mobius-dataAug/test_script/CSE-filesystem"
	# 원본 이미지가 저장되어 있는 로컬 경로
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
	print(" [ 'rotate' , ' distortion ' , 'zoom' ] ")
	global augty
	augty = str(input())
	if augty == 'rotate':
		print("Input left [0~20]")
		global left
		left = int(input())
		#왼쪽 회전 각도
		print("Input right [0~20]")
		global right
		right = int(input())
		#오른쪽 회전 각도
		print("Input amount :")
		global rotate_amount
		#sample 개수 
		rotate_amount = int(input())
		print("Input label :")
		global rotate_label
		#가공된 이미지 라벨
		rotate_label = str(input())
	if augty == 'zoom':
		print("Input min_factor")
		global minfactor
		#최소 확대
		minfactor = float(input())
		print("Input max_factor")
		global maxfactor
		#최대 확대
		maxfactor = float(input())
		print("Input amount :")
		global zoom_amount
		zoom_amount = int(input())
		print("Input label :")
		global zoom_label
		zoom_label = str(input())
	if augty == 'distortion':
		print("Input width")
		global width
		#왜곡 범위 설정 - 너비
		width = int(input())
		print("Input height")
		global height
		#왜곡 범위 설정 - 높이
		height = int(input())
		print("Input magnitude")
		global magnitude
		#왜곡  설정 
		magnitude = int(input())
		print("Input amount :")
		global distortion_amount
		distortion_amount = int(input())
		print("Input label :")
		global distortion_label
		distortion_label = str(input())
	print("Input targetpath :")
	global targetpath
	targetpath = input()
	print("Target Path is /virtualStore/classifier/",targetpath)
	if augty == 'rotate':
		print(select_name)
		payload = {
			"m2m:da": {
			"rn": rn,
		    "augty": augty,
		    "srsrc": "/virtualStore/classifier/target/"+select_name,
		    "augprm": {
		        "max_left_rotation": left,
		        "max_right_rotation": right,
		        "amount": rotate_amount,
		        "label": rotate_label
		    },
		    "trgrsrc": "/virtualStore/classifier/"+targetpath
		}
	    }
	if augty == 'zoom':
		print(select_name)
		payload = {
			"m2m:da": {
			"rn": rn,
		    "augty": augty,
		    "srsrc": "/virtualStore/classifier/target/"+select_name,
		    "augprm": {
		        "min_factor": minfactor,
		        "max_factor": maxfactor,
		        "amount": zoom_amount,
		        "label": zoom_label
            },
            "trgrsrc": "/virtualStore/classifier/"+targetpath
        }

    }
	
	if augty == 'distortion':
		print(select_name)
		payload = {
			"m2m:da": {
			"rn": rn,
		    "augty": augty,
		    "srsrc": "/virtualStore/classifier/target/"+select_name,
		    "augprm": {
		        "height": height,
		        "width": width,
			"magnitude" : magnitude,
		        "amount": distortion_amount,
		        "label": distortion_label
            },
            "trgrsrc": "/virtualStore/classifier/"+targetpath
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
