import cv2
import mediapipe as mp
import numpy as np
import sounddevice as sd

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

samplerate = 44100

def play_tone(freq):

    duration = 0.1
    t = np.linspace(0,duration,int(samplerate*duration),False)

    tone = np.sin(freq * 2 * np.pi * t)

    sd.play(tone,samplerate)
    sd.wait()


while True:

    success,img = cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:

        for handLms in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(img,handLms,mp_hands.HAND_CONNECTIONS)

            h,w,c = img.shape

            lm = handLms.landmark[8]  # index finger tip

            x = int(lm.x * w)
            y = int(lm.y * h)

            cv2.circle(img,(x,y),10,(255,0,0),-1)

            # convert vertical position into frequency
            freq = np.interp(y,[0,h],[800,200])

            play_tone(freq)

            cv2.putText(img,f"Freq:{int(freq)} Hz",(50,100),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    cv2.imshow("Gesture Music Instrument",img)

    if cv2.waitKey(1)==27:
        break