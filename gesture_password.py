import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

tip_ids = [4,8,12,16,20]

password = ["FIST","PEACE","THUMB"]
input_sequence = []

def fingers_up(landmarks):

    fingers = []

    # thumb
    if landmarks[tip_ids[0]][1] > landmarks[tip_ids[0]-1][1]:
        fingers.append(1)
    else:
        fingers.append(0)

    # other fingers
    for i in range(1,5):
        if landmarks[tip_ids[i]][2] < landmarks[tip_ids[i]-2][2]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers


while True:

    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(imgRGB)

    gesture = ""

    if results.multi_hand_landmarks:

        for handLms in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(img,handLms,mp_hands.HAND_CONNECTIONS)

            h,w,c = img.shape
            landmarks = []

            for id,lm in enumerate(handLms.landmark):

                cx,cy = int(lm.x*w), int(lm.y*h)
                landmarks.append((id,cx,cy))

            fingers = fingers_up(landmarks)

            # gesture rules
            if fingers == [0,0,0,0,0]:
                gesture = "FIST"

            elif fingers == [0,1,1,0,0]:
                gesture = "PEACE"

            elif fingers == [1,0,0,0,0]:
                gesture = "THUMB"


    if gesture != "":
        if len(input_sequence)==0 or gesture != input_sequence[-1]:
            input_sequence.append(gesture)


    if len(input_sequence) > len(password):
        input_sequence.pop(0)


    status = "LOCKED"

    if input_sequence == password:
        status = "UNLOCKED"


    cv2.putText(img,"Password:"+str(password),(10,40),
                cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)

    cv2.putText(img,"Input:"+str(input_sequence),(10,80),
                cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,255),2)

    cv2.putText(img,status,(10,130),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)

    cv2.imshow("Gesture Password",img)

    if cv2.waitKey(1)==27:
        break
