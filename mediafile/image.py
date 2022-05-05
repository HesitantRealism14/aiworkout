####aiworkout
import cv2
import time
import numpy as np
import Posenangle as pm



pose_ =str(input("Enter your exercise : "))
stage = None
detector = pm.poseDetector()
while True:
    #img = cv2.resize(img, (1280,720))
    img = cv2.imread('test/deadlift_184.jpg')
    img = detector.findPose(img)
    lmList = detector.findPosition(img , False)

    #print(lmList)
    if len(lmList) != 0:
        if pose_ == '1':
            ####################
            #---------------------#
            right_leg_angle = detector.findAngle(img, 23, 25, 27)
            left_leg_angle = detector.findAngle(img, 24, 26, 28)

            percent_ = np.interp(right_leg_angle,(170,290),(0,100))
            percent_ = np.interp(left_leg_angle,(170,290),(0,100))
            cv2.putText(img,str(int(percent_ )),(50, 50),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),2)
            #----------------------#
            if right_leg_angle > 150:
                stage = "up"
                cv2.putText(img, stage,
                    (65,70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (67,255,78), 2, cv2.LINE_AA )
            if right_leg_angle < 45 :
                stage="down"
                cv2.putText(img, stage,
                    (65,75),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (89,255,159), 2, cv2.LINE_AA )


        elif pose_ == '2':

            right_leg_angle = detector.findAngle(img, 24, 26, 28)
            #left_leg_angle = detector.findAngle(img, 23, 25, 27)

            percent_ = np.interp(right_leg_angle,(20,180),(0,100))
            #percent_ = np.interp(left_leg_angle,(170,290),(0,100))
            cv2.putText(img,str(int(percent_ )),(50, 50),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),2)

            if right_leg_angle > 150:
                stage = "up"
                cv2.putText(img, stage,
                    (65,70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (67,255,255), 2, cv2.LINE_AA )
            if right_leg_angle < 50 :
                stage="down"
                cv2.putText(img, stage,
                    (65,75),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (89,255,255), 2, cv2.LINE_AA )

#bench press
        elif pose_ == '3':
            stage = None
            arm_angle = detector.findAngle(img,16,14,12)
            #arm_angle = detector.findAngle(img,11,13,15)
            percent_ = np.interp(arm_angle,(20,180),(0,100))
            cv2.putText(img,str(int(percent_ )),(50, 50),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),2)
            if arm_angle > 150:
                stage = "up"
                cv2.putText(img, stage,
                    (65,70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (67,255,78), 2, cv2.LINE_AA )
            if arm_angle < 45 :
                stage="down"
                cv2.putText(img, stage,
                    (65,75),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (89,255,159), 2, cv2.LINE_AA )

                #print(stage)
            # Stage data
            #cv2.putText(img, 'STAGE', (65,52),
                    #cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 1, cv2.LINE_AA)





    cv2.imshow('image',img)
    cv2.waitKey(1)
    #cv2.destroyAllWindows()
