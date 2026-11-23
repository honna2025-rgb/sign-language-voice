
import cv2
import mediapipe as mp

# Initialize MediaPipe
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not available")
    exit()

# Finger tip IDs
tip_ids = [4, 8, 12, 16, 20]

# Password
password = ["FIST", "PEACE", "THUMB"]
input_sequence = []

# Frame validation
stable_frames = 6
release_frames = 6

current_gesture = ""
gesture_counter = 0

waiting_for_release = False
release_counter = 0


# Detect fingers
def fingers_up(landmarks, handedness):

    fingers = []

    # Thumb detection
    if handedness == "Right":

        if landmarks[4][1] < landmarks[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

    else:

        if landmarks[4][1] > landmarks[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

    # Other four fingers
    for i in range(1, 5):

        if landmarks[tip_ids[i]][2] < landmarks[tip_ids[i] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers


# Main loop
while True:

    success, img = cap.read()

    if not success:
        break

    # Mirror camera
    img = cv2.flip(img, 1)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(imgRGB)

    gesture = ""

    if results.multi_hand_landmarks:

        for index, handLms in enumerate(results.multi_hand_landmarks):

            mp_draw.draw_landmarks(
                img,
                handLms,
                mp_hands.HAND_CONNECTIONS
            )

            h, w, c = img.shape

            landmarks = []

            for id, lm in enumerate(handLms.landmark):

                cx = int(lm.x * w)
                cy = int(lm.y * h)

                landmarks.append((id, cx, cy))

            handedness = results.multi_handedness[index].classification[0].label

            fingers = fingers_up(landmarks, handedness)

            # Gesture recognition
            if fingers == [0, 0, 0, 0, 0]:
                gesture = "FIST"

            elif fingers == [0, 1, 1, 0, 0]:
                gesture = "PEACE"

            elif fingers == [1, 0, 0, 0, 0]:
                gesture = "THUMB"

            elif fingers == [1, 1, 1, 1, 1]:
                gesture = "OPEN"

    # Multi-frame validation
    if gesture == current_gesture and gesture != "":
        gesture_counter += 1

    else:
        current_gesture = gesture
        gesture_counter = 1 if gesture != "" else 0

    stable_gesture = ""

    if gesture_counter >= stable_frames:
        stable_gesture = current_gesture

    # Gesture release validation
    if waiting_for_release:

        if stable_gesture == "OPEN":
            release_counter += 1

        else:
            release_counter = 0

        if release_counter >= release_frames:

            waiting_for_release = False
            release_counter = 0

    # Accept a new gesture
    else:

        if stable_gesture in password:

            input_sequence.append(stable_gesture)

            waiting_for_release = True

            # Keep only three gestures
            if len(input_sequence) > len(password):
                input_sequence.pop(0)

    # Check password
    status = "LOCKED"

    if input_sequence == password:
        status = "UNLOCKED"

    # Display password
    cv2.putText(
        img,
        "Password: " + str(password),
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    # Display input
    cv2.putText(
        img,
        "Input: " + str(input_sequence),
        (10, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 255),
        2
    )

    # Display detected gesture
    cv2.putText(
        img,
        "Gesture: " + (stable_gesture if stable_gesture else "Detecting"),
        (10, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 0),
        2
    )

    # Display status
    color = (0, 255, 0) if status == "UNLOCKED" else (0, 0, 255)

    cv2.putText(
        img,
        status,
        (10, 170),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        3
    )

    cv2.putText(
        img,
        "Show OPEN PALM between gestures",
        (10, 215),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    cv2.putText(
        img,
        "Press R to reset | ESC to exit",
        (10, 250),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    cv2.imshow("Gesture Password", img)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        break

    if key == ord('r'):

        input_sequence = []
        current_gesture = ""
        gesture_counter = 0
        waiting_for_release = False
        release_counter = 0


# Release resources
cap.release()
hands.close()
cv2.destroyAllWindows()
