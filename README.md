# 🎨 Virtual Doodle

A webcam-powered drawing app controlled entirely by hand gestures! Draw, erase, change colors, resize brushes, and clear the canvas — all with your fingers in front of your webcam.

---

## 🚀 Features

- ✍️ Draw using your index finger
- 🧽 Erase using two fingers
- 🎨 Select colors by pointing at swatches
- 📏 Resize brush using three fingers (move up/down)
- 🖐️ Clear canvas with five fingers
- 🗣️ Voice feedback for every action using `pyttsx3`

---

## 🧠 Gesture Controls

| Gesture                          | Action                         |
|----------------------------------|--------------------------------|
| ✍️ Index finger up               | Draw mode                      |
| ✌️ Index + middle fingers up     | Erase mode                     |
| 🖐️ All 5 fingers up              | Clear canvas                   |
| 🥘 3 fingers (index, middle, ring) | Resize brush (move up/down)   |
| ☛ Point at color block           | Select color                   |

---

## 🔧 Setup Instructions

### 1. Clone this repository

```bash
git clone https://github.com/your-username/gesture-drawing-app.git
cd gesture-drawing-app
```

### 2. Install Dependencies

Create a virtual environment (optional but recommended), then install:

```bash
pip install streamlit opencv-python mediapipe numpy pyttsx3
```

> Or create a `requirements.txt` with:
```txt
streamlit
opencv-python
mediapipe
numpy
pyttsx3
```

And install with:
```bash
pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
streamlit run drawing_app.py
```

- A Streamlit app will open in your browser.
- Check **"Start Drawing"** to enable the camera and start gesture control.

---

## 📁 Project Structure

```
gesture-drawing-app/
├── drawing_app.py         # Main Streamlit app
├── README.md              # This file
└── requirements.txt       # List of dependencies (optional)
```

---

## 🛠 Troubleshooting

### ❌ `RuntimeError: run loop already started`

- This is a known issue with `pyttsx3`.
- It’s resolved in this project using `threading` to avoid blocking.

### ⚠️ Camera not working or black screen?

- Try changing the video backend in `cv2.VideoCapture(0)`:
  ```python
  cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # for Windows
  ```
- Ensure no other app is using the webcam.
- Restart your machine or browser tab.

---

## 🧰 Tech Used

- [Streamlit](https://streamlit.io/)
- [MediaPipe Hands](https://google.github.io/mediapipe/)
- [OpenCV](https://opencv.org/)
- [pyttsx3](https://pyttsx3.readthedocs.io/)
- [NumPy](https://numpy.org/)

---

## 📜 License

MIT License. Free to use, modify, and share.

---

## 👤 Author

Made with ❤️ by **techbuddy**  
🔗 GitHub: [@techinbuddy09](https://github.com/techinbuddy09)
