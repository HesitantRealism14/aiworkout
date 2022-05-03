import cv2
import time
import PoseModule as pm

cap = cv2.VideoCapture('test/plank_woman.jpg')
pTime = 0
detector = pm.poseDetector()
while True:
    success,img = cap.read()
    img = detector.findPose(img)
    lmList = detector.findPosition(img,draw=False)
    if len(lmList) != 0 :
        print(lmList[23])
        print(lmList[24])
        cv2.circle(img,(lmList[23][1],lmList[23][2]),15,(255,0,0),cv2.FILLED)
        cv2.circle(img,(lmList[24][1],lmList[24][2]),15,(0,0,255),cv2.FILLED)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,
                    (255,0,0),3)

    cv2.imshow('image',img)
    cv2.waitKey(1)
