import cv2
import mediapipe as mp
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities

device = AudioUtilities.GetSpeakers()
volume = device.EndpointVolume

print(f"Audio output: {device.FriendlyName}")
print(f"- Muted: {bool(volume.GetMute())}")
print(f"- Volume level: {volume.GetMasterVolumeLevel()} dB")
print(f"- Volume range: {volume.GetVolumeRange()[0]} dB - {volume.GetVolumeRange()[1]} dB")
volume.SetMasterVolumeLevel(-20.0, None)

cap =cv2.VideoCapture(0)
MpHands = mp.solutions.hands
Hands =MpHands.Hands()
while True:
    success,img=cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result = Hands.process(imgRGB)
    
    
    if result.multi_hand_landmarks :
        hand=result.multi_hand_landmarks[0]
        mp.solutions.drawing_utils.draw_landmarks(img,hand,MpHands.HAND_CONNECTIONS)
        lmlist=[]
        for id , lm in enumerate(hand.landmark):
            h,w,c=img.shape
            cx,cy=int(lm.x*w),int(lm.y*h)
            lmlist.append([id,cx,cy])
        if len(lmlist)>0:
            x1,y1=lmlist[4][1],lmlist[4][2]
            x2,y2=lmlist[8][1],lmlist[8][2]
            cx,cy=(x1+x2)//2,(y1+y2)//2
            cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
            cv2.circle(img,(x2,y2),10,(255,0,255),cv2.FILLED)
            cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)
            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
            length = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
            vol = np.interp(length, [30, 150], [-65.25, 0.0])
            volume.SetMasterVolumeLevel(vol, None)
    cv2.imshow('image',img)  # Commented out - OpenCV GUI not available
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break