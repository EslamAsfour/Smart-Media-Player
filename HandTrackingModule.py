import cv2 as cv
import mediapipe as mp
import time as t
from scipy.spatial import distance as dist
import VLC 


'''
Hand Detector class contain 4 main functions
1- initial function
2- FindHand
3- FindPosition
4- Main Function
'''
class HandDetector():

     def __init__ (self, VLC , mode=False, maxHands=1, detectionCon=0.5, trackCon=0.5  ):

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
          self.VLC = VLC

          #Formality before start using this module

          self.mpHands = mp.solutions.mediapipe.python.solutions.hands
          self.hands=self.mpHands.Hands(self.mode ,self.maxHands ,self.detectionCon , self.trackCon )

          #Formality before start using this module
          self.mpDraws=mp.solutions.mediapipe.python.solutions.drawing_utils 
          
          #! Conters
          self.PauseFlag = False
          self.VolUpCounter = 0
          self.VolDownCounter = 0
          self.ToggleCounter = 0
          self.FullScreenCounrter = 0
          self.MinimizeCounter = 0
          
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


     def FindPositions (self,img , HandNo=0 ,draw =False):

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
            
     #! Takes img and do action based on the gesture
     def GestureAction(self , img):
          
         
          img=self.FindHands(img)
          lmList=self.FindPositions(img,draw=False)
          if len(lmList) != 0:
               no_one_dist = int(dist.euclidean((lmList[8][1],lmList[8][2]),(lmList[0][1],lmList[0][2])))
               no_two_dist = int(dist.euclidean((lmList[12][1],lmList[12][2]),(lmList[0][1],lmList[0][2])))
               no_three_dist = int(dist.euclidean((lmList[16][1],lmList[16][2]),(lmList[0][1],lmList[0][2])))
               no_four_dist = int(dist.euclidean((lmList[20][1],lmList[20][2]),(lmList[0][1],lmList[0][2])))
               
               
               # print("4","3","2","1")
               # print(int(no_four_dist),int(no_three_dist),int(no_two_dist),int(no_one_dist))
               #! Toggle Play and Pause
               if (lmList[8][2]- lmList[4][2]) > 50  and (lmList[12][2]- lmList[4][2]) > 50:
                    self.ToggleCounter = self.ToggleCounter +1
                    self.VolDownCounter = 0
                    self.VolUpCounter = 0
                    self.FullScreenCounrter = 0
                    self.MinimizeCounter = 0
               #! Volume Up
               elif lmList[8][1] - lmList[5][1] > 100:
                    print("Side")
                    self.VolDownCounter = self.VolDownCounter +1 
                    self.ToggleCounter = 0
                    self.VolUpCounter = 0
                    self.FullScreenCounrter = 0
                    self.MinimizeCounter = 0
                    
               #! Volume Down
               elif lmList[5][1] - lmList[8][1] > 100:
                    print("Other Side")  
                    self.VolUpCounter = self.VolUpCounter+1 
                    self.ToggleCounter = 0
                    self.VolDownCounter = 0
                    self.FullScreenCounrter = 0
                    self.MinimizeCounter = 0
               #! Full Screen
               elif  int(no_one_dist/no_two_dist) >= 2 and int(no_one_dist/no_three_dist) >= 2 and int(no_one_dist/no_four_dist) >= 2:
                    print("Number 1") 
                    self.FullScreenCounrter = self.FullScreenCounrter +1
                    self.ToggleCounter = 0
                    self.VolDownCounter = 0
                    self.VolUpCounter = 0
                    self.MinimizeCounter = 0
                    '''
                    #! Minimize 
                    elif int(no_two_dist/no_one_dist) >= 1 and int(no_one_dist/no_three_dist) >= 2 and int(no_one_dist/no_four_dist) >= 2:
                         print("Number 2")
                         self.ToggleCounter = 0
                         self.VolDownCounter = 0
                         self.VolUpCounter = 0
                         self.FullScreenCounrter = 0
                         self.MinimizeCounter = self.MinimizeCounter +1 
                         
                    elif (int(no_two_dist / no_one_dist) >= 1 and int(no_two_dist / no_three_dist) >= 1 and int(no_one_dist / no_four_dist) >= 2) or (int(no_two_dist / no_three_dist) >= 1 and int(no_two_dist / no_four_dist) >= 1 and int(no_four_dist / no_one_dist) > 0.8):
                         print("Number 3")
                         self.ToggleCounter = 0
                         self.VolDownCounter = 0
                         self.VolUpCounter = 0
                         self.FullScreenCounrter = 0
                         self.MinimizeCounter = 0
                    
                    elif int(no_two_dist / no_three_dist) >= 1 and int(no_two_dist / no_four_dist) >= 1 and int(no_one_dist / no_four_dist) > 0.5:
                         print("Number 4")
                         self.ToggleCounter = 0
                         self.VolDownCounter = 0
                         self.VolUpCounter = 0
                         self.FullScreenCounrter = 0
                         self.MinimizeCounter = 0
                    '''     
                    #bug when the hand is closed the condition is still true.
               else:
                    print("No")
                    self.ToggleCounter = 0
                    self.VolDownCounter = 0
                    self.VolUpCounter = 0
                    self.FullScreenCounrter = 0
                    self.MinimizeCounter = 0
                    
               
               
               #! Check for Action
               #! Toggle  Play/Pause
               if self.ToggleCounter > 20:
                    if VLC.Get_Status_VLC() == True:
                         self.PauseFlag = True
                    else : 
                         self.PauseFlag = False
                    self.ToggleCounter =0
                    VLC.toggle_VLC(self.VLC)
                    return 50
               #! Volume Up
               elif self.VolUpCounter > 15:
                    self.VolUpCounter = 0
                    VLC.VolUP_VLC(self.VLC)
                    return 30
               #! Volume Down
               elif self.VolDownCounter > 15:
                    self.VolDownCounter = 0
                    VLC.VolDown_VLC(self.VLC)
                    return 30
               #If no Action 
               #! Volume Up
               elif self.FullScreenCounrter > 20:
                    self.FullScreenCounrter = 0
                    VLC.TFS_VLC(self.VLC)
                    return 30
               
               return 0
          return 0
          



'''
def main():


          #Initiallization for Time
          pTime=0
          cTime=0

          cap =cv.VideoCapture(0)
          detector =HandDetector()

          while True:
             success, img = cap.read()

             img=detector.FindHands(img)
             lmList=detector.FindPositions(img,draw=False)

             #Displaying The Frame Rate Per Second
             cTime=t.time()
             fps= 1/ (cTime-pTime)
             pTime=cTime

             cv.putText(img , str(int(fps)),(10,70),cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
             #number 1

             if len(lmList) != 0:
               no_one_dist = int(dist.euclidean((lmList[8][1],lmList[8][2]),(lmList[0][1],lmList[0][2])))
               no_two_dist = int(dist.euclidean((lmList[12][1],lmList[12][2]),(lmList[0][1],lmList[0][2])))
               no_three_dist = int(dist.euclidean((lmList[16][1],lmList[16][2]),(lmList[0][1],lmList[0][2])))
               no_four_dist = int(dist.euclidean((lmList[20][1],lmList[20][2]),(lmList[0][1],lmList[0][2])))
               
               
               # print("4","3","2","1")
               # print(int(no_four_dist),int(no_three_dist),int(no_two_dist),int(no_one_dist))
               #! Check for Thumbs Up 
               
               if (lmList[8][2]- lmList[4][2]) > 50  and (lmList[12][2]- lmList[4][2]) > 50:
                    print("Thumbs Up!")
               elif lmList[8][1] - lmList[5][1] > 100:
                    print("Side")
               elif lmList[5][1] - lmList[8][1] > 100:
                    print("Other Side")     
               elif  int(no_one_dist/no_two_dist) >= 2 and int(no_one_dist/no_three_dist) >= 2 and int(no_one_dist/no_four_dist) >= 2:
                    print("Number 1")
               elif int(no_two_dist/no_one_dist) >= 1 and int(no_one_dist/no_three_dist) >= 2 and int(no_one_dist/no_four_dist) >= 2:
                    print("Number 2")
               elif (int(no_two_dist / no_one_dist) >= 1 and int(no_two_dist / no_three_dist) >= 1 and int(no_one_dist / no_four_dist) >= 2) or (int(no_two_dist / no_three_dist) >= 1 and int(no_two_dist / no_four_dist) >= 1 and int(no_four_dist / no_one_dist) > 0.8):
                    print("Number 3")
               elif int(no_two_dist / no_three_dist) >= 1 and int(no_two_dist / no_four_dist) >= 1 and int(no_one_dist / no_four_dist) > 0.5:
                    print("Number 4")
                    #bug when the hand is closed the condition is still true.
               else:
                    print("No")

             #Display our Image
             cv.imshow("Image",img)
             cv.waitKey(1)
               

     if __name__ == "__main__":
        main()

'''