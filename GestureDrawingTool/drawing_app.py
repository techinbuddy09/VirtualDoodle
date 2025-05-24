import cv2
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

xp, yp = 0, 0
imgCanvas = None
brushThickness = 8
eraserThickness = 30
drawColor = (255, 0, 255)  # fixed color (purple)
mode = "draw"

def fingers_up(lmList):
    fingers = []
    tipIds = [4, 8, 12, 16, 20]

    # Thumb
    if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Fingers
    for id in range(1, 5):
        fingers.append(1 if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2] else 0)
    return fingers

def smooth_point(prev, curr, smooth_factor=0.7):
    return int(prev + smooth_factor * (curr - prev))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    if imgCanvas is None:
        imgCanvas = np.zeros_like(img)

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

                x1, y1 = lmList[8][1], lmList[8][2]

                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                x1 = smooth_point(xp, x1)
                y1 = smooth_point(yp, y1)

                # Clear canvas if all 5 fingers are up
                if totalFingers == 5:
                    imgCanvas = np.zeros_like(img)
                    xp, yp = 0, 0
                    mode = "clear"

                # Drawing mode: only index finger up
                elif indexUp == 1 and middleUp == 0:
                    mode = "draw"
                    cv2.circle(img, (x1, y1), 10, drawColor, cv2.FILLED)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                    xp, yp = x1, y1

                # Eraser mode: index and middle fingers up
                elif indexUp == 1 and middleUp == 1:
                    mode = "erase"
                    cv2.circle(img, (x1, y1), 20, (0, 0, 0), cv2.FILLED)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), (0, 0, 0), eraserThickness)
                    xp, yp = x1, y1

                else:
                    xp, yp = 0, 0

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    else:
        xp, yp = 0, 0

    # Combine canvas and webcam
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    cv2.putText(img, f'Mode: {mode}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, drawColor, 2)

    cv2.imshow("Gesture Drawing", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        cv2.imwrite("gesture_drawing.png", imgCanvas)
        print("Saved drawing to gesture_drawing.png")

cap.release()
cv2.destroyAllWindows()
