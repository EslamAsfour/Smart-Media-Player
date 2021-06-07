import cv2
import mediapipe as mp
from scipy.spatial import distance as dist
import VLC 
import time as t

from HandTrackingModule import HandDetector
from FaceDetection import FaceDetection 
import os



VLC_1 = VLC.Open_VLC()

cap=cv2.VideoCapture(0)

FaceObj = FaceDetection(VLC_1)
HandObj = HandDetector(VLC_1)
os.environ["GLOG_minloglevel"] ="3"

UserPaused = False
WaitNoCommand = 0
while cap.isOpened() :
    ret,frame=cap.read()
    if WaitNoCommand == 0 :
        if HandObj.PauseFlag == False:
            FaceObj.FaceDetection(frame)
        WaitNoCommand = HandObj.GestureAction(frame)
        
    else:
        WaitNoCommand = WaitNoCommand - 1
    
    print("=============================================================="+str(HandObj.PauseFlag))    
    
    cv2.imshow("cam view",frame)
    if cv2.waitKey(10) &  0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()


