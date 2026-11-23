
import threading
import time
import cv2
import mediapipe as mp
import pyttsx3

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
tip_ids = [4, 8, 12, 16, 20]

speech_lock = threading.Lock()


def speak(text):
    clean = text.strip()
    if not clean:
        return

    def _run():
        with speech_lock:
            try:
                engine = pyttsx3.init()
                engine.setProperty("rate", 165)
                engine.setProperty("volume", 1.0)
                print(f"[SPEAKING]: {clean}")
                engine.say(clean)
                engine.runAndWait()
                engine.stop()
            except Exception as err:
                print(f"[SPEECH ERROR]: {err}")

    threading.Thread(target=_run, daemon=True).start()


def get_fingers_up(landmarks, handedness_label):
    fingers = []
    if handedness_label == "Right":
        fingers.append(1 if landmarks[tip_ids[0]][1] < landmarks[tip_ids[0] - 1][1] else 0)
    else:
        fingers.append(1 if landmarks[tip_ids[0]][1] > landmarks[tip_ids[0] - 1][1] else 0)

    for i in range(1, 5):
        fingers.append(1 if landmarks[tip_ids[i]][2] < landmarks[tip_ids[i] - 2][2] else 0)
    return tuple(fingers)


SINGLE_HAND_GESTURES = {
    (1, 1, 1, 1, 1): "HELLO",
    (0, 1, 0, 0, 0): "WHAT'S UP",
    (0, 1, 1, 0, 0): "HOW ARE YOU",
    (1, 0, 0, 0, 0): "I'M GOOD",
    (1, 1, 0, 0, 1): "SLAY",
    (0, 0, 0, 0, 1): "LOWKEY",
    (1, 0, 0, 0, 1): "VIBE",
    (0, 1, 1, 1, 0): "W",
    (1, 1, 0, 0, 0): "L",
    (0, 1, 0, 0, 1): "GOAT",
    (0, 1, 1, 1, 1): "BET",
    (1, 1, 1, 0, 0): "BRO",
    (0, 0, 1, 1, 1): "NO CAP",
    (0, 0, 0, 0, 0): "PERIODT",
}

TWO_HAND_GESTURES = {
    ((1, 1, 1, 1, 1), (1, 1, 1, 1, 1)): "SHEESH",
    ((0, 1, 1, 0, 0), (0, 1, 1, 0, 0)): "FR",
    ((1, 0, 0, 0, 0), (1, 0, 0, 0, 0)): "BUSSIN",
    ((0, 1, 0, 0, 0), (0, 1, 0, 0, 0)): "SUS",
    ((1, 1, 0, 0, 1), (1, 1, 0, 0, 1)): "RIZZ",
    ((0, 1, 1, 1, 0), (0, 1, 1, 1, 0)): "BIG W",
    ((1, 0, 0, 0, 1), (1, 0, 0, 0, 1)): "CHILL",
    ((0, 1, 0, 0, 1), (0, 1, 0, 0, 1)): "ICONIC",
    ((0, 1, 1, 1, 1), (0, 1, 1, 1, 1)): "FAM",
    ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0)): "SAY LESS",
}

sentence = ""
last_gesture = ""
last_added_time = 0.0
COOLDOWN = 1.6

while True:
    success, img = cap.read()
    if not success or img is None:
        continue

    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    current_gesture = ""
    detected_hands = []

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_lms, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
            lm_list = [[idx, int(lm.x * w), int(lm.y * h)] for idx, lm in enumerate(hand_lms.landmark)]
            label = handedness.classification[0].label
            fingers = get_fingers_up(lm_list, label)
            detected_hands.append(fingers)

        if len(detected_hands) == 1:
            current_gesture = SINGLE_HAND_GESTURES.get(detected_hands[0], "")
        elif len(detected_hands) >= 2:
            pair = (detected_hands[0], detected_hands[1])
            rev_pair = (detected_hands[1], detected_hands[0])
            current_gesture = TWO_HAND_GESTURES.get(pair) or TWO_HAND_GESTURES.get(rev_pair, "")

        now = time.time()
        if current_gesture and (
            current_gesture != last_gesture or (now - last_added_time) > COOLDOWN
        ):
            sentence += current_gesture + " "
            last_gesture = current_gesture
            last_added_time = now
            speak(current_gesture)

    visible_sentence = sentence[-55:]

    cv2.rectangle(img, (0, 0), (w, 55), (25, 25, 25), -1)
    cv2.putText(
        img,
        f"Detected: {current_gesture}",
        (15, 38),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.95,
        (0, 255, 0),
        2,
    )

    cv2.rectangle(img, (0, h - 80), (w, h), (20, 20, 20), -1)
    cv2.putText(
        img,
        f"Sentence: {visible_sentence}",
        (15, h - 42),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (255, 255, 255),
        2,
    )
    cv2.putText(
        img,
        "[S] Speak Sentence  [SPACE] Space  [BACKSPACE] Delete  [C] Clear  [Q] Quit",
        (15, h - 12),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,
        (180, 180, 180),
        1,
    )

    cv2.imshow("Gen Z Sign Language Sentence Builder", img)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break
    elif key == ord("s"):
        speak(sentence)
    elif key == 32:
        sentence += " "
    elif key == 8:
        sentence = sentence[:-1]
    elif key == ord("c"):
        sentence = ""
        last_gesture = ""

cap.release()
cv2.destroyAllWindows()