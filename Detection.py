import cv2
import mediapipe as mp
from scipy.spatial import distance as dist
import VLC 

VLC_1 = VLC.Open_VLC()

mp_drawing= mp.solutions.drawing_utils
mp_faceMesh=mp.solutions.face_mesh
cap=cv2.VideoCapture(0)
# Eye Closed Frame Counter
Closed_Eye_Count = 0
Opened_Eye_Count = 0
# No Face Counter
No_Face_Counter = 0
with mp_faceMesh.FaceMesh(min_detection_confidence=0.5,min_tracking_confidence=0.5) as FaceMesh:
    while cap.isOpened() :
        ret,frame=cap.read()
        img=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=FaceMesh.process(img)
        img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:
            for faceLms in results.multi_face_landmarks:
                
                # Reset Noface Counter
                No_Face_Counter = 0
                
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
                    Closed_Eye_Count = Closed_Eye_Count + 1 
                    Opened_Eye_Count = 0
                else: 
                    Closed_Eye_Count = 0
                    Opened_Eye_Count = Opened_Eye_Count + 1 
                    
                    
                if Closed_Eye_Count > 100 or Opened_Eye_Count > 100  or Opened_Eye_Count < 0 or Closed_Eye_Count < 0 :
                    Opened_Eye_Count = 0
                    Closed_Eye_Count = 0
                
                
                if Closed_Eye_Count > 30 :
                    VLC.Pause_VLC(VLC_1)
                elif Opened_Eye_Count > 30:
                    VLC.Play_VLC(VLC_1)
                else : 
                    pass
        else : 
            #! No Face Pause
            No_Face_Counter = No_Face_Counter + 1
            if No_Face_Counter > 30 :
                VLC.Pause_VLC(VLC_1)
                
                    
        img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        cv2.imshow("cam view",img)
        if cv2.waitKey(10) &  0xFF==ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
