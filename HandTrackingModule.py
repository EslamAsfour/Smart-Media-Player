import cv2 as cv
import mediapipe as mp
import time as t


'''
Hand Detector class contain 4 main functions
1- initial function
2- FindHand
3- FindPosition
4- Main Function
'''
class HandDetector():

     def __init__ (self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):

          """
          Arguments :
          mode : state Whether to detect all the time or track and detect , Flase means detect Then Track
          maxHands : Max No.of Hands
          detectionCon : Detection confidence
          trackCon : Tracking confidence

          """

          self.mode=mode
          self.maxHands=maxHands
          self.detectionCon=detectionCon
          self.trackCon=trackCon


          #Formality before start using this module

          self.mpHands = mp.solutions.mediapipe.python.solutions.hands
          self.hands=self.mpHands.Hands(self.mode ,self.maxHands ,self.detectionCon , self.trackCon )

          #Formality before start using this module
          self.mpDraws=mp.solutions.mediapipe.python.solutions.drawing_utils 

     def FindHands (self , img , draw= True):

          """
          Arguments :
          1 - Image 
          2 - option to draw connections between landmarks

          """
          ImageRGB= cv.cvtColor(img,cv.COLOR_BGR2RGB)
          self.results= self.hands.process(ImageRGB)

          #print(results.multi_hand_landmarks)
          if self.results.multi_hand_landmarks:
               #take hand by hand if there is more than one
               for handLms in self.results.multi_hand_landmarks: 
                    if draw:
                         #draw landmarks on each hand
                         self.mpDraws.draw_landmarks(img,handLms , self.mpHands.HAND_CONNECTIONS)  
          return img               


     def FindPositions (self,img , HandNo=0 ,draw =True):

          """
          Arguments :
          1- Image 
          2- Hand Number
          3- Draw cicles around landmarks

          """
          lmList =[]
          #print(results.multi_hand_landmarks)
          if self.results.multi_hand_landmarks:

               myHand=self.results.multi_hand_landmarks[HandNo]
               #Getting each landmark with it's Id
               for id,lm in enumerate(myHand.landmark):
                    h,w,c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id,cx,cy])
                    if draw:
                       cv.circle(img,(cx,cy),12,(0,0,0),cv.FILLED)


          return lmList          



     def main() :

          #Initiallization for Time
          pTime=0
          cTime=0

          cap =cv.VideoCapture(0)
          detector =HandDetector()

          while True:
             success, img = cap.read()

             img=detector.FindHands(img)
             lmList=detector.FindPositions(img)
             if len(lmList) != 0:
                 print(lmList[4])



             #Displaying The Frame Rate Per Second
             cTime=t.time()
             fps= 1/ (cTime-pTime)
             pTime=cTime

             cv.putText(img , str(int(fps)),(10,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
          
             #Dsiplay our Image
             cv.imshow("Image",img)
             cv.waitKey(1)
               

     if __name__ == "__main__":
        main()


































cap =cv.VideoCapture(0)

#Formality before start using this module
mpHands = mp.solutions.mediapipe.python.solutions.hands
mpDraws=mp.solutions.mediapipe.python.solutions.drawing_utils  

#object from our model to use class Hands
hands=mpHands.Hands()                                        


#Initiallization for Time
pTime=0
cTime=0

while True:
     success, img = cap.read()
     ImageRGB= cv.cvtColor(img,cv.COLOR_BGR2RGB)
     results= hands.process(ImageRGB)

     #print(results.multi_hand_landmarks)
     if results.multi_hand_landmarks:
          #take hand by hand if there is more than one
          for handLms in results.multi_hand_landmarks: 
               #Getting each landmark with it's Id
               for id,lm in enumerate(handLms.landmark):
                    h,w,c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    print(id, cx, cy)
                    
                    cv.circle(img,(cx,cy),12,(0,0,0),cv.FILLED)
               #draw landmarks on each hand
               mpDraws.draw_landmarks(img,handLms , mpHands.HAND_CONNECTIONS)       



     #Displaying The Frame Rate Per Second
     cTime=t.time()
     fps= 1/ (cTime-pTime)
     pTime=cTime

     cv.putText(img , str(int(fps)),(10,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
 
     #Dsiplay our Image
     cv.imshow("Image",img)
     cv.waitKey(1)
