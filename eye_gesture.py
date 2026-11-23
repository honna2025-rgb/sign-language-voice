
import cv2
import mediapipe as mp
import numpy as np


# Initialize Face Mesh
mp_face = mp.solutions.face_mesh

face_mesh = mp_face.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Unable to open webcam")
    exit()


# Blink variables
blink_count = 0
eye_closed_frames = 0

EAR_THRESHOLD = 0.21
BLINK_FRAMES = 2


# Calculate Eye Aspect Ratio
def eye_aspect_ratio(eye):

    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])

    if C == 0:
        return 0

    ear = (A + B) / (2.0 * C)

    return ear


# Eye landmark indexes
eye_ids = [33, 160, 158, 133, 153, 144]


while True:

    success, img = cap.read()

    if not success:
        break

    img = cv2.flip(img, 1)

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(imgRGB)

    ear = 0
    gesture = "NO BLINK"

    if results.multi_face_landmarks:

        for face_landmarks in results.multi_face_landmarks:

            h, w, _ = img.shape

            eye = []

            # Get eye landmarks
            for id in eye_ids:

                x = int(face_landmarks.landmark[id].x * w)
                y = int(face_landmarks.landmark[id].y * h)

                eye.append(np.array([x, y]))

                cv2.circle(
                    img,
                    (x, y),
                    2,
                    (0, 255, 0),
                    -1
                )

            # Calculate EAR
            ear = eye_aspect_ratio(eye)

            # Blink detection
            if ear < EAR_THRESHOLD:

                eye_closed_frames += 1

                gesture = "EYE CLOSED"

            else:

                if eye_closed_frames >= BLINK_FRAMES:

                    blink_count += 1

                eye_closed_frames = 0

                gesture = "EYES OPEN"

            # Display gesture
            if blink_count == 1:
                gesture = "COME"

            elif blink_count >= 2:
                gesture = "GO"

            if eye_closed_frames > 15:
                gesture = "OK"

            if ear > 0.35:
                gesture = "ANGRY"

    # Display information
    cv2.putText(
        img,
        f"EAR: {ear:.2f}",
        (30, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        img,
        f"Blinks: {blink_count}",
        (30, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    cv2.putText(
        img,
        gesture,
        (30, 130),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        img,
        "Press R to reset | ESC to exit",
        (30, 180),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.imshow("Eye Gesture Control", img)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        break

    if key == ord('r'):
        blink_count = 0
        eye_closed_frames = 0


# Release resources
cap.release()
face_mesh.close()
cv2.destroyAllWindows()
