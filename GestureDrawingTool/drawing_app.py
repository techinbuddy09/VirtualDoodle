import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import pyttsx3

st.set_page_config(page_title="Gesture Drawing App", layout="wide")
st.title("🎨 Gesture-Based Drawing App")
run = st.checkbox("Start Drawing")
FRAME_WINDOW = st.image([])

def speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except RuntimeError:
        pass

# Hand detection
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

def fingers_up(lmList):
    fingers = []
    tipIds = [4, 8, 12, 16, 20]
    if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
        fingers.append(1)
    else:
        fingers.append(0)
    for id in range(1, 5):
        fingers.append(1 if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2] else 0)
    return fingers

def smooth_point(prev, curr, smooth_factor=0.7):
    return int(prev + smooth_factor * (curr - prev))

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

xp, yp = 0, 0
imgCanvas = None
brushThickness = 8
eraserThickness = 30
drawColor = (255, 0, 255)
mode = "draw"

colors = [(255, 0, 255), (255, 0, 0), (0, 255, 0), (0, 255, 255), (0, 0, 0)]
colorNames = ["Purple", "Blue", "Green", "Yellow", "Eraser"]
colorPositions = [(i * 100 + 10, 10) for i in range(len(colors))]

if run:
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        if imgCanvas is None:
            imgCanvas = np.zeros_like(img)

        for i, (x, y) in enumerate(colorPositions):
            cv2.rectangle(img, (x, y), (x + 80, y + 80), colors[i], cv2.FILLED)
            cv2.putText(img, colorNames[i], (x + 5, y + 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                lmList = []
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append((id, cx, cy))

                if len(lmList) > 12:
                    fingerState = fingers_up(lmList)
                    totalFingers = sum(fingerState)

                    indexUp = fingerState[1]
                    middleUp = fingerState[2]
                    ringUp = fingerState[3]

                    x1, y1 = lmList[8][1], lmList[8][2]

                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1

                    x1 = smooth_point(xp, x1)
                    y1 = smooth_point(yp, y1)

                    if indexUp == 1 and middleUp == 0:
                        for i, (x, y) in enumerate(colorPositions):
                            if x < x1 < x + 80 and y < y1 < y + 80:
                                drawColor = colors[i]
                                mode = "erase" if drawColor == (0, 0, 0) else "draw"
                                speak(f"{colorNames[i]} selected")

                    if totalFingers == 5:
                        imgCanvas = np.zeros_like(img)
                        xp, yp = 0, 0
                        mode = "clear"
                        speak("Canvas cleared")

                    elif fingerState == [0, 1, 1, 1, 0]:
                        mode = "resize"
                        y_movement = y1 - yp
                        if abs(y_movement) > 15:
                            if y_movement < 0:
                                brushThickness += 2
                                brushThickness = min(50, brushThickness)
                                speak("Brush size increased")
                            else:
                                brushThickness -= 2
                                brushThickness = max(2, brushThickness)
                                speak("Brush size decreased")
                        xp, yp = x1, y1

                    elif indexUp == 1 and middleUp == 0:
                        mode = "draw"
                        cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                        xp, yp = x1, y1

                    elif indexUp == 1 and middleUp == 1:
                        mode = "erase"
                        cv2.line(imgCanvas, (xp, yp), (x1, y1), (0, 0, 0), eraserThickness)
                        xp, yp = x1, y1

                    else:
                        xp, yp = 0, 0

                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        else:
            xp, yp = 0, 0

        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)

        cv2.putText(img, f'Mode: {mode}', (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, drawColor, 2)
        FRAME_WINDOW.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
else:
    st.info("👆 Check 'Start Drawing' to activate the camera.")
