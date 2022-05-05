####aiworkout
import cv2
import time
import numpy as np
import Posenangle as pm



pose_ =str(input("Enter your exercise : "))
cap = cv2.VideoCapture('test/female-.mp4')
detector = pm.poseDetector()
while True:

    ref, img = cap.read()
    #img = cv2.resize(img, (1280,720))
    img = detector.findPose(img)
    lmList = detector.findPosition(img , False)
    #print(lmList)
    if len(lmList) != 0:
        if pose_ == 'squat':
            ####################
            #---------------------#
            R_angle = detector.findAngle(img, 24, 26, 28)
            L_angle = detector.findAngle(img, 12, 24, 26)
            #----------------------#
            #getting the max and min range of motion in our pose
            percent_ = np.interp(R_angle,(179,280),(0,100))
            percent_ = np.interp(L_angle,(180,280),(0,100))
            print(percent_, R_angle)
            print(percent_, L_angle)


            # detector.findAngle(img, 12,11,24,26)
        elif pose_ == 'deadlift':
            detector.findAngle(img,24,26,28)
            detector.findAngle(img,23,25,27)


        elif pose_ == 'bench press':
            ben_R =detector.findAngle(img,16,14,12)
            ben_L= detector.findAngle(img,11,13,15)

            ######
            percent_ = np.interp(ben_R,(179,280),(0,100))
            percent_ = np.interp(ben_L,(180,280),(0,100))
            print(percent_, ben_R)
            # print(percent_, L_angle)


    cv2.imshow('image',img)
    cv2.waitKey(1)
    #cv2.destroyAllWindows()
