import paho.mqtt.client as mqtt
import Augmentor
import requests
import base64
import json
import time
import glob
import os

url = "http://localhost:7579/Mobius"
host = '127.0.0.1'
mqtt_port = 1883



def do_augment(daAttr):
    global select_name
    select_name3=daAttr['srsrc']
    select_name2=select_name3.split("/")
    select_name=select_name2[4]
    select_name=select_name.strip(".jpg")
    augment_img="CSE-filesystem/"+select_name
    #원본이미지가 저장되어 있는 경로를 Pipeline에 입력해 주어야 하므로 원하는 이미지를 입력받고 해당 경로를 저장한다
    if daAttr['augty'] == 'rotate':
        p = Augmentor.Pipeline(augment_img)
        prm = daAttr['augprm']
        p.rotate(probability=1, max_left_rotation=int(prm['max_left_rotation']),
                    max_right_rotation=int(prm['max_right_rotation']))
        p.sample(int(prm['amount']))
        #print(" --data aug okay-- ")
    if daAttr['augty'] == 'zoom':
        p = Augmentor.Pipeline(augment_img)
        prm = daAttr['augprm']
        p.zoom(probability=1, min_factor=prm['min_factor'],
                    max_factor=prm['max_factor'])
        p.sample(int(prm['amount']))
        #print(" --data aug okay-- ")
    if daAttr['augty'] == 'distortion':
        p = Augmentor.Pipeline(augment_img)
        prm = daAttr['augprm']
        p.random_distortion(probability=1, grid_width=prm['width'], grid_height=prm['height'], magnitude=prm['magnitude'])
        p.sample(int(prm['amount']))
        #print(" --data aug okay-- ")
    else:
        print("augmentType " + daAttr['augty'] + " is not implemented")
    global targetpath
    targetpath3=daAttr['trgrsrc']
    targetpath2=targetpath3.split("/")
    targetpath=targetpath2[3]
	
    


def encode_img(filename):
    f = open(filename, "rb")
    fileContent = f.read()
    byteArr = bytearray(fileContent)
    imgbyte = base64.b64encode(byteArr)
    f.close()
    return imgbyte

def make_cnt(targetpath):
    create_container(targetpath)
def create_container(targetpath):
    payload = {
        "m2m:cnt": {
		"rn": targetpath,
		"lbl": [targetpath],
		"mbs": 999999999
		}
	}
    headers = {
	  'Accept': 'application/json',
	  'X-M2M-RI': '12345',
	  'X-M2M-Origin': 'SvirtualStore',
	  'Content-Type': 'application/vnd.onem2m-res+json; ty=3'
	}
    #print("MAKE CNT OKAY",targetpath)
    response = requests.post(url+'/virtualStore/classifier', json=payload, headers=headers)
    print(response.text)


def create_cin(rn, filename, targetpath):
	payload = {
		"m2m:cin": {
			"rn": rn,
			"con": encode_img(filename)
        }
    }
	headers = {
        'Accept': 'application/json',
        'X-M2M-RI': '12345',
        'X-M2M-Origin': 'SCSF',
        'Content-Type': 'application/vnd.onem2m-res+json; ty=4'
    }
	time.sleep(1)
	#print("this is rn : ",rn)
	#print("this is filename : ",filename)
	#print("TargetPath")
	#print(targetpath[3])
	response = requests.post(url + '/virtualStore/classifier/'+targetpath, json=payload, headers=headers)
	print(response.text)


def create_target(label):
    folder_path = "/home/yamewrong/Desktop/lab/dataAug/mobius-dataAug/test_script/CSE-filesystem/"+select_name+"/output"
    #augmentation된 결과가 위 floder_path에 저장되어 있으므로 해당 경로를 저장해 준다.
    folder_path2 = "/home/yamewrong/Desktop/lab/dataAug/mobius-dataAug/test_script"
    #augmentation된 결과물의 이름을 변경하고 저장하고 싶은 경로에 저장하기 위해 원하는 경로를 floder_path2에 저장한다.
    folder_list = os.listdir(folder_path)
    # print(folder_list)
    a = 1
   
    make_cnt(targetpath)
    train_path = "/home/yamewrong/Desktop/lab/dataAug/mobius-dataAug/test_script/train"
    #train 폴더 경로를 저장
    os.mkdir(train_path+"/"+label)
    #Augmentation 할 때 마다 결과를 저장할 폴더를 train 하위에 생성
    for filename in folder_list:
        rn = str(label) + "_aug" + str(a)

        # print("this is rn",rn,"*****")
        # filename = '/train/'+str(rn)+'.jpg'
        file_name1 = folder_path + '/' + filename
        file_name2 = folder_path2 + '/train/'+ label + '/' + rn + '.jpg'
        os.rename(file_name1, file_name2)
        # print("this is filename",filename,"*****")
        create_cin(rn, file_name2,targetpath)

        a += 1


def on_connect(client, userdata, flag, rc):
    if rc != 0:
        print("Bad connection, return code %d", rc)
    else:
        print("Connected to MQTT brocker")


def on_message(client, userdata, message):
    print("message topic=", message.topic)
    payload = message.payload.decode("utf-8")
    payload = json.loads(payload)
    rep = payload['pc']['m2m:sgn']['nev']['rep']
    rootnm = next(iter(rep))
    if rootnm == 'm2m:da':
        do_augment(rep['m2m:da'])
        print(rep['m2m:da']['augprm']['label'])
        create_target(rep['m2m:da']['augprm']['label'])


if __name__ == "__main__":
    client = mqtt.Client('csf')
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host, mqtt_port)
    client.subscribe("/oneM2M/req/Mobius2/virtualStore/da/json")
    print("listening...")
    client.loop_forever()
