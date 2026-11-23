# ✨ Gen Z Sign Language & Slang Sentence Builder (With Offline Voice)

![Gen Z Sign Language Sentence Builder](Gen%20Z%20Sign%20Language%20Sentence%20Builder.png)

Turn hand gestures into full sentences—and hear them spoken out loud—in real time using your webcam. Built with **OpenCV**, **MediaPipe**, and **pyttsx3**, this project recognizes **24 single-hand and two-hand finger patterns**, maps them to everyday greetings and Gen Z slang, builds live sentences on screen, and speaks words or entire sentences offline.

---

## 🎯 Key Features

* **Live Sentence Composition:** Hold a gesture for ~1.6 seconds to append words or phrases smoothly without spamming duplicate entries.
* **1-Hand & 2-Hand Recognition:** Combines 14 single-hand gestures and 10 two-hand gestures for **24 total recognized words and slang phrases**.
* **Offline Voice Output (`pyttsx3`):** Speaks newly added words/phrases and reads the full sentence out loud on demand without external API keys.
* **Instant Sentence Editing:** Add spaces, delete characters, clear the sentence, or quit using single-key shortcuts while the camera window is focused.

---

## 🛠️ Tech Stack

* **Python** (run inside a local `.venv` virtual environment)
* **OpenCV (`opencv-python`)** — Webcam capture (`cv2.CAP_DSHOW`), mirrored display, landmark rendering, and HUD overlays
* **MediaPipe (`mediapipe`)** — Real-time 21-point hand landmark detection and left/right handedness classification
* **pyttsx3** — Offline text-to-speech engine on Windows

---

## 🚀 Setup & Run (Windows + VS Code)

1. **Create and activate a virtual environment** inside the project folder:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

   1. **Create and activate a virtual environment** inside the project folder:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
**Install dependencies:**
   python -m pip install opencv-python mediapipe pyttsx3
**run the application:**
   python sign_lan.py
   ⌨️ Keyboard ControlsClick once on the Gen Z Sign Language Sentence Builder window to focus it, then press:KeyActionSSpeak the full current sentence out loudSpaceAdd a spaceBackspaceDelete the last characterCClear the sentence and reset the last gesture stateQQuit and close the webcam window🖐️ 
Gesture Reference (24 Gestures)Finger tuples follow (Thumb, Index, Middle, Ring, Pinky) where 1 = extended/up and 0 = folded/down.
One-Hand Gestures (14)Finger PatternHand ShapeOutput(1, 1, 1, 1, 1)Open palm (all 5 fingers up)HELLO(0, 1, 0, 0, 0)Index finger upWHAT'S UP(0, 1, 1, 0, 0)Peace sign (index + middle)HOW ARE YOU(1, 0, 0, 0, 0)Thumbs upI'M GOOD(1, 1, 0, 0, 1)Spider-Man / ILY sign (thumb, index, pinky)SLAY(0, 0, 0, 0, 1)Pinky up onlyLOWKEY(1, 0, 0, 0, 1)Shaka sign (thumb + pinky)VIBE(0, 1, 1, 1, 0)Three middle fingers upW(1, 1, 0, 0, 0)L-shape (thumb + index)L(0, 1, 0, 0, 1)Rock horns (index + pinky)GOAT(0, 1, 1, 1, 1)Four fingers up (thumb folded)BET(1, 1, 1, 0, 0)Thumb + index + middleBRO(0, 0, 1, 1, 1)Middle, ring, and pinky upNO CAP(0, 0, 0, 0, 0)Closed fistPERIODTTwo-Hand Gestures (10)Both Hands ShapeOutputBoth open palms (1, 1, 1, 1, 1)SHEESHBoth peace signs (0, 1, 1, 0, 0)FRBoth thumbs up (1, 0, 0, 0, 0)BUSSINBoth index fingers up (0, 1, 0, 0, 0)SUSBoth Spider-Man signs (1, 1, 0, 0, 1)RIZZBoth 3-finger W signs (0, 1, 1, 1, 0)BIG WBoth Shaka signs (1, 0, 0, 0, 1)CHILLBoth rock horns (0, 1, 0, 0, 1)ICONICBoth 4-finger signs (0, 1, 1, 1, 1)FAMBoth closed fists (0, 0, 0, 0, 0)SAY LESS
💡 Quick TroubleshootingCamera index: If index 0 does not open, update cv2.VideoCapture(0, cv2.CAP_DSHOW) to cv2.VideoCapture(1, cv2.CAP_DSHOW) in sign_lan.py.Audio output: Confirm Windows output volume/device and ensure an English TTS voice is installed in Windows speech settings.Detection accuracy: Use bright, even lighting and keep your hand clearly framed in front of the webcam.
   
