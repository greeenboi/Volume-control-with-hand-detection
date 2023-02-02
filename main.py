#wireless sound control project by suvan

#inporting libraries
import numpy as np
import math
import cv2
import mediapipe as mp


from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#taking input from webcam using the videcapture function
cap = cv2.VideoCapture(0)
mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

#defining the size of the output window
width, height = 1100,1100 # Width of camera, #Height of Camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

#initializing the sound control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))



#while loop to check for any false values
while True:
       success,img = cap.read()
       imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
       res=hands.process(imgRGB)
       #drawing the landmarks on the hand if present
       if(res.multi_hand_landmarks):
           for handLms in res.multi_hand_landmarks:
               lmList=[]
               for id,lm in enumerate (handLms.landmark):
                   h,w,c = img.shape
                   cx, cy=int(lm.x*w),int(lm.y*h)
                   #rint(id,cx,cy)
                   lmList.append([id,cx,cy])
                   #print(lmList)
                   mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
           if lmList:#if landmarks are drawn, the lines/circles are drawn
                x1,y1=lmList[4][1],lmList[4][2]
                x2,y2=lmList[8][1],lmList[8][2]
               
                cv2.circle(img,(x1,y1),10,(59,182,104),cv2.FILLED)
                cv2.circle(img,(x2,y2),10,(59,182,104),cv2.FILLED)
                cv2.putText(img,"Index Tip",(x2,y2),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),1,cv2.LINE_AA,True)
                cv2.putText(img,"Thumb Tip",(x1,y1),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),1,cv2.LINE_AA,True)
                
                cv2.line(img,(x1,y1),(x2,y2),(200,100,100),2)
                
                length = math.hypot(x2-x1,y2-y1)
                #print(length)
                z1=(x1+x2)//2
                z2=(y1+y2)//2
                if (length >50 and length <450):
                    slen="{0:.2f} pixels".format(length)
                    cv2.putText(img,slen,(z1,z2),cv2.FONT_HERSHEY_PLAIN,1,(255,255,0),2,cv2.LINE_AA,True)
                if length <50:
                    cv2.circle(img,(z1,z2),10,(255,0,255),cv2.FILLED)
                    cv2.putText(img,"Volume 0%",(z1,z2),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3,cv2.LINE_AA,True)
                        
                volRange = volume.GetVolumeRange()
                minVol = volRange[0]
                maxVol = volRange[1]
                #changing the volume based on the length btw index and thumb
                vol = np.interp(length,[50,300],[minVol,maxVol])
                volume.SetMasterVolumeLevel(vol,None)
                VolPer=np.interp(length,[50,300],[0,100])
           #
                VolBar=np.interp(length,[50,300],[400,150])
                v="{0:.2f}".format(abs(VolPer))
                cv2.rectangle(img,(50,150),(85,400),(126,58,234),3)
                cv2.rectangle(img,(85,int(VolBar)),(50,150),(126,58,234),cv2.FILLED)
                cv2.putText(img,str(v),(85,400),cv2.FONT_HERSHEY_PLAIN,1,(30,40,40),1,cv2.LINE_AA,True)
           #
       imge = cv2.rotate(img, cv2.ROTATE_180)#displaying the video output 
       image=cv2.flip(imge,1)
       cv2.imshow("Camera Feed",image)
       cv2.waitKey(1)
