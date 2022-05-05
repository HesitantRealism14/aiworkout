from email import message
import time
import cv2
import mediapipe as mp
import math
class poseDetector():

    def __init__(self,mode=False,upBody=False,smooth=True,
                 detectionCon=False,trackCon=0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpPose = mp.solutions.pose
        self.mpDraw = mp.solutions.drawing_utils
        self.pose = self.mpPose.Pose(self.mode,self.upBody,self.smooth,self.detectionCon,self.trackCon)

    def findPose(self,img,draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self,img,draw=True):
        self.lmList=[]
        if self.results.pose_landmarks:
            for id,lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c = img.shape
                #print(id,lm)
                cx,cy = int(lm.x * w) , int(lm.y * h)
                self.lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),10,(255,0,0),cv2.FILLED)
        return self.lmList

    def findAngle(self,img,p1,p2,p3,draw=True):

        #get landmarks
        x1,y1 = self.lmList[p1][1:]
        x2,y2 = self.lmList[p2][1:]
        x3,y3 = self.lmList[p3][1:]

        #calculate angles
        angle = math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))

        if angle > 180:
            angle = 360 - angle
        #print(angle)

        if draw:

            cv2.line(img,(x1,y1),(x2,y2),(245,117,66),2)
            cv2.line(img,(x3,y3),(x2,y2),(245,117,66),2)

            cv2.circle(img,(x1,y1),5,(245,66,230),cv2.FILLED)
            cv2.circle(img,(x1,y1),10,(255,0,0),2)
            cv2.circle(img,(x2,y2),5,(245,66,230),cv2.FILLED)
            cv2.circle(img,(x2,y2),10,(255,0,0),2)
            cv2.circle(img,(x3,y3),5,(245,66,230),cv2.FILLED)
            cv2.circle(img,(x3,y3),10,(255,0,0),2)

            cv2.putText(img,str(int(angle)),(x2-20,y2-20),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),2)

        return angle














# def main():
#     cap = cv2.VideoCapture('test/video2.mp4')
#     pTime = 0
#     detector = poseDetector()
#     while True:
#         success,img = cap.read()
#         img = detector.findPose(img)
#         lmList = detector.findPosition(img,draw=False)
#         if len(lmList) != 0 :
#             print(lmList[15])
#             print(lmList[23])
#             cv2.circle(img,(lmList[15][1],lmList[15][2]),15,(0,0,255),cv2.FILLED)
#             cv2.circle(img,(lmList[23][1],lmList[23][2]),15,(0,0,255),cv2.FILLED)

#         cTime = time.time()
#         fps = 1/(cTime-pTime)
#         pTime = cTime

        # cv2.putText(img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,
        #             (255,0,0),3)

        # cv2.imshow('image',img)
        # cv2.waitKey(1)


if __name__ == "__main__":
    main()
