
import cv2
import mediapipe as mp


class HandTracker:

    def __init__(self):

        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.mpDraw = mp.solutions.drawing_utils

    def detect_hands(self, img):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = self.hands.process(imgRGB)

        landmarks = []

        if results.multi_hand_landmarks:

            for handLms in results.multi_hand_landmarks:

                self.mpDraw.draw_landmarks(
                    img,
                    handLms,
                    self.mpHands.HAND_CONNECTIONS
                )

                hand_landmarks = []

                h, w, c = img.shape

                for id, lm in enumerate(handLms.landmark):

                    cx = int(lm.x * w)
                    cy = int(lm.y * h)

                    hand_landmarks.append((id, cx, cy))

                landmarks.append(hand_landmarks)

        return img, landmarks


# Run independently
if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    tracker = HandTracker()

    while True:

        success, img = cap.read()

        if not success:
            break

        img, landmarks = tracker.detect_hands(img)

        cv2.imshow("Hand Tracking", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

    tracker.hands.close()

    cv2.destroyAllWindows()
