####aiworkout
import cv2
import time
import numpy as np
import Posenangle as pm


#cap = cv2.VideoCapture('test/plank_woman.jpg')
pose_ =str(input("Enter your exercise : "))
detector = pm.poseDetector()
while True:
    img = cv2.imread('test/deadlift_127.jpg')
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img , False)
    #print(lmList)
    if len(lmList) != 0:
        if pose_ == 'squat':
            detector.findAngle(img,12,24,26 )
            # detector.findAngle(img, 12,11,24,26)
        elif pose_ == 'deadlift':
            detector.findAngle(img,12,24,26)
        elif pose_ == 'bench press':
            detector.findAngle(img,16,14,12)


    cv2.imshow('image',img)
    cv2.waitKey(1)
