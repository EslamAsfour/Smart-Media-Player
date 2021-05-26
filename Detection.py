import cv2
import mediapipe as mp
from scipy.spatial import distance as dist

mp_drawing= mp.solutions.drawing_utils
mp_faceMesh=mp.solutions.face_mesh
cap=cv2.VideoCapture(0)
with mp_faceMesh.FaceMesh(min_detection_confidence=0.5,min_tracking_confidence=0.5) as FaceMesh:

    while cap.isOpened() :
        ret,frame=cap.read()
        img=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=FaceMesh.process(img)
        #print(results.face_landmarks)
        img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:
            for faceLms in results.multi_face_landmarks:
                #faceLms=faceLms.landmark[0:150]
                #mp_drawing.draw_landmarks(img,faceLms,mp_faceMesh.FACE_CONNECTIONS,
                                          #mp_drawing.DrawingSpec(color=(0,255,0),thickness=1, circle_radius=2),
                x = []
                y = []
                # mp_drawing.DrawingSpec(color=(0,255,0),thickness=1, circle_radius=2))
                ih, iw, ic = img.shape
                lm=faceLms.landmark[246]
                x.append(int(lm.x * iw))
                y.append(int(lm.y * ih))
                lm=faceLms.landmark[173]
                x.append(int(lm.x * iw))
                y.append(int(lm.y * ih))
                lm=faceLms.landmark[159]
                x.append(int(lm.x * iw))
                y.append(int(lm.y * ih))
                lm=faceLms.landmark[145]
                x.append(int(lm.x * iw))
                y.append(int(lm.y * ih))

                img= cv2.line(img, (x[0],y[0]), (x[1],y[1]), (0,255,0), 1)
                img = cv2.line(img, (x[2], y[2]), (x[3], y[3]), (0, 255, 0), 1)
                A = dist.euclidean((x[2],y[2]), (x[3],y[3]))
                B = dist.euclidean((x[0], y[0]), (x[1], y[2]))
                C= A/B
                print(C)


        cv2.imshow("cam view",img)
        if cv2.waitKey(10) &  0xFF==ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
