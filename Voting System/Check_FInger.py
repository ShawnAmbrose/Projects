import numpy as np
import cv2, sys, os
from statistics import mode
import time
from datetime import date
from datetime import datetime
import sys, numpy, os
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
import serial

vein_chk = 1
fv_id = -1

buzzer = 26

try:
    f = PyFingerprint('COM3', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))



cam_set = 1

while cam_set:

    print('Waiting for finger...')
    while ( f.readImage() == False ):
        pass
    f.convertImage(0x01)
    result = f.searchTemplate()

    positionNumber = result[0]
    accuracyScore = result[1]

    print(positionNumber)

    if positionNumber == -1:
        print('No match found!')
    cam_set = 0
        
print('Completed')
sys.exit()
