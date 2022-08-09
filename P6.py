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


def retrieve_training_data(srsrc):
    payload = {}
    headers = {
        'Accept': 'application/json',
        'X-M2M-RI': '12345',
        'X-M2M-Origin': 'SvirtualStore'
    }
    print(srsrc)
    response = requests.get(url + srsrc, json=payload, headers=headers)
    data = response.json()
    byteArr = data['m2m:cin']['con']
    img_byte = base64.b64decode(byteArr)
    f = open("CSE-filesystem/1.jpg", "wb")
    f.write(img_byte)
    f.close()


def do_augment(daAttr):
    retrieve_training_data(daAttr['srsrc'])
    if daAttr['augty'] == 'rotate':
        pipe = Augmentor.Pipeline("CSE-filesystem")
        prm = daAttr['augprm']
        pipe.rotate(probability=1, max_left_rotation=int(prm['max_left_rotation']),
                    max_right_rotation=int(prm['max_right_rotation']))
        pipe.sample(int(prm['amount']))
        print(" --data aug okay-- ")
    else:
        print("augmentType " + daAttr['augty'] + " is not implemented")


def encode_img(filename):
    f = open(filename, "rb")
    fileContent = f.read()
    byteArr = bytearray(fileContent)
    imgbyte = base64.b64encode(byteArr)
    f.close()
    return imgbyte


def create_cin(rn, filename):
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
    print("this is rn : ",rn)
    print("this is filename : ",filename)
    response = requests.post(url + '/virtualStore/classifier/target', json=payload, headers=headers)
    print(response.text)


def create_target(label):
    folder_path = "/home/yamewrong/Desktop/lab/dataAug/mobius-dataAug/test_script/CSE-filesystem/output"
    folder_path2 = "/home/yamewrong/Desktop/lab/dataAug/mobius-dataAug/test_script"
    folder_list = os.listdir(folder_path)
    # print(folder_list)
    a = 1
    for filename in folder_list:
        rn = str(label) + "_aug" + str(a)

        # print("this is rn",rn,"*****")
        # filename = '/train/'+str(rn)+'.jpg'
        file_name1 = folder_path + '/' + filename
        file_name2 = folder_path2 + '/train/' + rn + '.jpg'
        os.rename(file_name1, file_name2)
        # print("this is filename",filename,"*****")
        create_cin(rn, file_name2)

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
