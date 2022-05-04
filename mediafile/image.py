####aiworkout
import cv2
import time
import numpy as np
import Posenangle as pm


#cap = cv2.VideoCapture('test/plank_woman.jpg')
pose_ =str(input("Enter your exercise : "))
cap = cv2.VideoCapture('test/production ID_5025965.mp4')
detector = pm.poseDetector()
while True:

    ref, img = cap.read()
    #img = cv2.resize(img, (1280,720))
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img , False)
    #print(lmList)
    if len(lmList) != 0:
        if pose_ == 'squat':
            ####################
            #---------------------#
            right_leg_angle = detector.findAngle(img, 24, 26, 28)
            left_leg_angle = detector.findAngle(img, 23, 25, 27)
            #----------------------#
            # detector.findAngle(img, 12,11,24,26)
        elif pose_ == 'deadlift':
            detector.findAngle(img,24,26,28)
            detector.findAngle(img,23,25,27)


        elif pose_ == 'bench press':
            detector.findAngle(img,16,14,12)
            detector.findAngle(img,11,13,15)


    cv2.imshow('image',img)
    cv2.waitKey(1)
    #cv2.destroyAllWindows()
