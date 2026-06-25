import numpy as np
import easygui
import cv2, sys, os
from statistics import mode
import time
from datetime import date
from datetime import datetime
import sys, numpy, os
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
import serial
import PySimpleGUI as sg

try:
    f = PyFingerprint('COM3', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

pl_count = 0

pcPath = r'C:\xampp\htdocs\dashboard'
pcFilePath = os.path.join(pcPath,'count.txt')
fo = open(pcFilePath,"w")
fo.write("0")
fo.close()

size = 4
haar_file = 'haarcascade_frontalface_default.xml'
datasets = 'datasets'
print('Please wait camera is opening...!')
(images, labels, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            label = id
            images.append(cv2.imread(path, 0))
            labels.append(int(label))
        id += 1
(width, height) = (130, 100)

(images, labels) = [np.array(lis) for lis in [images, labels]]

#model = cv2.face.FisherFaceRecognizer_create()
model = cv2.face.FisherFaceRecognizer_create()
model.train(images, labels)
id_list = []
unknown_count = 0

face_cascade = cv2.CascadeClassifier(haar_file)

# database
v_db_path = r'C:\xampp\htdocs\dashboard\people_server\v_db.txt'
db_f = open(v_db_path, "r")
l_data = db_f.readline()
db_f.close()

li_data = l_data.split(';')
print(li_data)

pl_data = {'id':[],'name':[],'st':[]}
for li_idx in range(0,len(li_data)):
    li_sub = li_data[li_idx].split(':')
    pl_data['id'].append(li_sub[0])
    pl_data['name'].append(li_sub[1])
    pl_data['st'].append(0)
    

print(pl_data)

while True:
    sg.theme('SandyBeach')
    layout_column = [
            [sg.Text('<<< Please Press Submit to Capture >>>')],
            [sg.Button('Continue'), sg.Button('  Exit  !')]
            ]
    layout = [[sg.Column(layout_column, element_justification='center')]]
                              
    window = sg.Window('Voting sys', layout)
    event, values = window.read()
    window.close()

    if event == '  Exit  !':
        print('Program Terminated...!')
        sys.exit()

    pl_id   = pl_data['id']
    pl_name = pl_data['name']
    pl_st   = pl_data['st']

    # Face Recognition
    '''sg.theme('SandyBeach')
    layout = [
            [sg.Text('Please enter your name!')],
            [sg.Text('Name', size =(15, 1)), sg.InputText()],
            [sg.Submit(), sg.Cancel()]
            ]
    
    window = sg.Window('Voting sys', layout)
    event, values = window.read()
    window.close()
    
    face_name = values[0]
    print(face_name)'''
    face_name = 'unknown'
    face_r = 1
    webcam = cv2.VideoCapture(0)
    while face_r:
        (_, im) = webcam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        #print('Module 2')
        for (x,y,w,h) in faces:
            #cv2.rectangle(im,(x,y),(x+w,y+h),(255,0,0),2)
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            prediction = model.predict(face_resize)
            #print (prediction[0],prediction[1])
            #cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 255), 3)
            #print(prediction[1])
            if prediction[1]<2500:
                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.putText(im,'%s - %.0f' % (names[prediction[0]],prediction[1]),(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
                id_list.append(names[prediction[0]])
            else:
                unknown_count = unknown_count + 1
                if unknown_count > 150:
                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 255), 3)
                    cv2.putText(im,'unknown',(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
                    unknown_count = 0
                    id_list.append('unknown')
                    face_r = 0
                    webcam.release()
                    cv2.destroyAllWindows()
                    print('Unknown Person!!')
                    #break
            if len(id_list) > 50:
                face_name = mode(id_list)
                print('Identified Person Name: '+ face_name)
                cv2.putText(im,face_name,(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
                plPath = r'C:\xampp\htdocs\dashboard'
                img_path = os.path.join(plPath,face_name + '.jpg')
                cv2.imwrite(img_path, im)
                id_list = []
                face_r = 0
                webcam.release()
                cv2.destroyAllWindows()
                print('Exit!')
                #break

        if face_r == 1:
            cv2.imshow('OpenCV', im)
            key = cv2.waitKey(10)
            if key == 27:
                break

    idx = 0
    match_idx = []
    for pl_face in pl_name:
        if face_name == pl_face:
            match_idx = idx
            break
        idx = idx + 1
        
    finger_set = 0
    if match_idx == []:
        print('Face id not found in data base!')
    else:
        if pl_st[match_idx] == '1':
            print('Face id already voted!')
        else:
            finger_set = 1
    
    if finger_set == 1:
        # Finger print recognition
        '''sg.theme('SandyBeach')
        layout = [
                [sg.Text('Please enter finger id')],
                [sg.Text('Fid', size =(15, 1)), sg.InputText()],
                [sg.Submit(), sg.Cancel()]
                ]
        
        window = sg.Window('Voting sys', layout)
        event, values = window.read()
        window.close()
        
        fin_id = values[0]
        print(fin_id)'''

        print('Waiting for finger...')
        while ( f.readImage() == False ):
            pass
        f.convertImage(0x01)
        result = f.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        fin_id = str(positionNumber)
        print(fin_id)
        
        vote_set = 0
        if fin_id !=  pl_id[match_idx]:
            print('Finger id & Face id not matching!')
        else:
            vote_set = 1

        if vote_set == 1:
            sg.theme('SandyBeach')
            layout = [
                    [sg.Text('Please select your vote! <A/B/C>')],
                    [sg.Text('Vote', size =(15, 1)), sg.InputText()],
                    [sg.Submit(), sg.Cancel()]
                    ]
            
            window = sg.Window('Voting sys', layout)
            event, values = window.read()
            window.close()

            pl_data['st'][match_idx] = '1'
            print(pl_data['st'][match_idx])

            pl_count = pl_count + 1
            print('Voting Done!')

            plPath = r'C:\xampp\htdocs\dashboard'
            plFilePath = os.path.join(pcPath,str(pl_count) + '.txt')

            plvote_data = pl_data['name'][match_idx] + ';' + pl_data['id'][match_idx] + ';' +\
                            pl_data['st'][match_idx] + ';' + pl_data['name'][match_idx] + '.jpg'

            pl_f = open(plFilePath, "w")
            pl_f.write(plvote_data)
            pl_f.close()
            
            pcPath = r'C:\xampp\htdocs\dashboard'
            pcFilePath = os.path.join(pcPath,'count.txt')
            fo = open(pcFilePath,"w")
            fo.write(str(pl_count))
            fo.close()

print('Completed')
sys.exit()
