import socket
import json
import base64
import os
import Augmentor

#폴더 따로 만들고 requirements 만들기
#함수로 분리

first_trigger_state = True
response_trigger_state = True

HOST = 'localhost' #'192.168.247.1' #socket(client) 통신, HOST IP는 사용 PC에 따라 달라질 수 있음.
PORT =  3105
#CNT_AIMLSVC = '/Mobius/tinyS/aiMLSvc/'
CNT_TRAININGDATA = 'trData'
CNT_DATAAUG = 'dataAug'

#HEADERS = {
#    'Accept': 'application/json',
#    'X-M2M-RI': 'tinyS100',
#    'X-M2M-Origin': 'StinyS',
#    'Content-Type': 'application/vnd.onem2m-res+json; ty=4'
#}

NAME = (HOST,PORT)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(NAME)

first_trigger_data = '{"ctname": "' + CNT_TRAININGDATA + '", "con": "hello"}' + '<EOF>' #server에 trData를 듣겠다고 인사
client_socket.send(first_trigger_data.encode('utf-8'))

while True:
    print('::WAIT')
    data = client_socket.recv(1000000)

    if first_trigger_state : # trigger를 걸면 first_trigger_data 2001 response 무시
        print("-- ", CNT_TRAININGDATA)
        first_trigger_state = False
        continue

    dec_data = data.decode('utf-8')
    #print(dec_data)
    jsonObj = json.loads(dec_data)
    #print(jsonObj['con'])
    #print(jsonObj['rn'])
    #print(jsonObj['rUri'])

    #save decoded trData resource to image file (trData.jpg) ; CWD/augmetedData 존재해야 함
    #CHECK ./augmetedData/RN-augT-augP/에 저장 augmented images 저장
    #CHECK trData.jpg는 삭제할 것, png?
    img_byte = base64.b64decode(jsonObj['con'])
    f = open("augmetedData\\trData.jpg", "wb")
    #f = open("trData.jpg", "wb")
    f.write(img_byte)
    f.close()

    #CHECK augmentation config file
    # https://www.youtube.com/watch?v=pyczpaJOuLU
    # augType : 'rotate'  ' distortion '  'zoom'
    # augParam :
    #path = os.path.realpath('trData.jpg')
    #path = os.path.realpath(os.getcwd())
    path = os.path.realpath('augmetedData\\')
    os.startfile(path)
    
    dataAugParam = {}

    print("Input augType No.")
    print(" [ '1. rotate' , '2. distortion ' , '3. zoom' ] ")
    augType = str(input())
    if augType == '1':
        augType = 'rotate'
        print("Input max_left_rotation [0~20]")
        dataAugParam['left'] = int(input())
        #왼쪽 회전 각도
        print("Input right [0~20]")
        dataAugParam['right'] = int(input())
        #오른쪽 회전 각도

    if augType == '2':
        augType = 'distortion'
        print("Input width")
        #왜곡 범위 설정 - 너비
        dataAugParam['width'] = int(input())
        print("Input height")
        #왜곡 범위 설정 - 높이
        dataAugParam['height'] = int(input())
        print("Input magnitude")
        #왜곡  설정 
        dataAugParam['magnitude'] = int(input())

    if augType == '3':
        augType = 'zoom'
        print("Input min_factor (1.1)")
        #최소 확대
        dataAugParam['min_factor'] = float(input())
        print("Input max_factor (9.9)")
        #최대 확대
        dataAugParam['max_factor'] = float(input())

    print("Input amount :")
    dataAugParam['amount'] = int(input())
    print("Input label :")
    dataAugParam['label'] = str(input())
        
    #create cin(dataAug(request))
    dataAugCon = {
        "status" : "request",
        "srcRrc" : jsonObj['rUri'],
        "augType" : augType,
        "augprm" : dataAugParam
    }

    dataAug_sok = '{"ctname": "dataAug", "con": '+ json.dumps(dataAugCon) +'}' + '<EOF>'
    client_socket.send(dataAug_sok.encode('utf-8'))

    #directory = 'augmetedData//' + jsonObj['rn'] + '-' + augType
    directory = 'augmetedData//'
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory.' + directory)

    p = Augmentor.Pipeline(directory)

    if augType == 'rotate':
        p.rotate(probability=1, max_left_rotation=dataAugParam['left'], max_right_rotation=dataAugParam['right'])

    if augType == 'distortion':
        p.random_distortion(probability=1, grid_width=dataAugParam['width'], grid_height=dataAugParam['height'], magnitude=dataAugParam['magnitude'])

    if augType == 'zoom':
        p.zoom(probability=1, min_factor=dataAugParam['min_factor'], max_factor=dataAugParam['max_factor'])
    
    p.sample(dataAugParam['amount'])

    # CHECK 상위 폴더로 위치 변경
    augDataPath = directory+ jsonObj['rn'] + '-' + augType
    os.rename(directory + 'output', augDataPath)
    os.startfile(os.path.realpath(augDataPath))

    #create cin(dataAug(done))
    dataAugCon = {
        "status" : "done",
        "augDataPath" : augDataPath,
        "srcRrc" : jsonObj['rUri'],
        "augType" : augType,
        "augprm" : dataAugParam
    }

    dataAug_sok = '{"ctname": "dataAug", "con": '+ json.dumps(dataAugCon) +'}' + '<EOF>'
    client_socket.send(dataAug_sok.encode('utf-8'))

    #CHECK trData.jpg 삭제
    #CHECK 여러번 동작 가능하도록

    if response_trigger_state:  #2001, cin
        for i in range(0,3):
            data = client_socket.recv(1000000)