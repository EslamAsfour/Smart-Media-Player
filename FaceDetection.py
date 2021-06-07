import cv2
import mediapipe as mp
from scipy.spatial import distance as dist
import VLC 





class FaceDetection():
    def __init__(self,VLC):
        self.mp_drawing= mp.solutions.drawing_utils
        self.mp_faceMesh=mp.solutions.face_mesh
        # Eye Closed Frame Counter
        self.Closed_Eye_Count = 0
        self.Opened_Eye_Count = 0
        # No Face Counter
        self.No_Face_Counter = 0
        self.VLC = VLC

    def FaceDetection(self,frame):
        with self.mp_faceMesh.FaceMesh(min_detection_confidence=0.5,min_tracking_confidence=0.5) as FaceMesh:
            img=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            results=FaceMesh.process(img)
            img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            if results.multi_face_landmarks:
                for faceLms in results.multi_face_landmarks:
                    
                    # Reset Noface Counter
                    self.No_Face_Counter = 0
                    
                    # Left Eye Key Points
                    NeededPoint = [246, 173, 159, 145] 
                    x = []
                    y = []
                    
                    ih, iw, ic = img.shape
                    
                    for i in NeededPoint :
                        lm=faceLms.landmark[i]
                        x.append(int(lm.x * iw))
                        y.append(int(lm.y * ih))
                    

                    # Eye Vertical And Horizontal Line
                    img= cv2.line(img, (x[0],y[0]), (x[1],y[1]), (0,255,0), 1)
                    img = cv2.line(img, (x[2], y[2]), (x[3], y[3]), (0, 255, 0), 1)
                    # Calc Eye Aspect Ratio
                    A = dist.euclidean((x[2],y[2]), (x[3],y[3]))
                    B = dist.euclidean((x[0], y[0]), (x[1], y[2]))
                    # Eye Aspect Ratio
                    C= (A*2) / B
                    
                    #! Eye Counter 
                    if (C*10) < 6 :
                        self.Closed_Eye_Count = self.Closed_Eye_Count + 1 
                        self.Opened_Eye_Count = 0
                    else: 
                        self.Closed_Eye_Count = 0
                        self.Opened_Eye_Count = self.Opened_Eye_Count + 1 
                        
                        
                    if self.Closed_Eye_Count > 100 or self.Opened_Eye_Count > 100  or self.Opened_Eye_Count < 0 or self.Closed_Eye_Count < 0 :
                        self.Opened_Eye_Count = 0
                        self.Closed_Eye_Count = 0
                    
                    
                    if self.Closed_Eye_Count > 30 :
                        VLC.Pause_VLC(self.VLC)
                    elif self.Opened_Eye_Count > 30:
                        VLC.Play_VLC(self.VLC)
                    else : 
                        pass
            else : 
                #! No Face Pause
                self.No_Face_Counter = self.No_Face_Counter + 1
                if self.No_Face_Counter > 30 :
                    VLC.Pause_VLC(self.VLC)
                    


'''
#! Test Case
VLC_1 = VLC.Open_VLC()

cap=cv2.VideoCapture(0)

FaceObj =FaceDetection(VLC_1)

while cap.isOpened() :
        ret,frame=cap.read()
        FaceObj.FaceDetection(frame)
        cv2.imshow("cam view",frame)
        if cv2.waitKey(10) &  0xFF==ord('q'):
            break
cap.release()
cv2.destroyAllWindows()


'''