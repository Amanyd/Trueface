# This is face identification software
# 🤖 Face Recognition Based Servo Control System
### Project Title: Development of Face Identification Software and Its Application in Humanoid Robot

---

## 🧠 Overview

This project demonstrates a real-time **face recognition system** integrated with **Arduino-controlled servo motor**, designed as part of a 6-week training under the ECE Department, Northern Railway Workshop, Lucknow.

When the system recognizes a registered face through the GUI interface, it sends a signal (`1`) to the Arduino via serial communication, triggering a servo motor to move (e.g., simulate robotic response). If the face is unrecognized, the system sends `0`, and the servo remains still.

---

## ⚙️ Technologies Used

| Component         | Technology            |
|------------------|-----------------------|
| GUI              | Python Tkinter        |
| Face Detection   | OpenCV                |
| Face Recognition | face_recognition (dlib) |
| Hardware         | Arduino Uno           |
| Motor            | Servo Motor (SG90)    |
| Communication    | Serial (pyserial)     |

---

## 🗂️ Project Structure

face_robot_project/
│
├── gui_main.py # Main GUI file (Tkinter-based)
├── register_faces.py # Module to register new faces
├── recognizer.py # Face recognition logic
├── arduino_control.ino # Arduino code (uploaded via Arduino IDE)
├── encodings.pkl # Serialized facial encodings
├── requirements.txt # Python libraries list
├── README.md # This file
├── /known_faces/ # Folder storing registered face images

markdown
Copy
Edit

---

## 🖼️ System Workflow

1. **Face Registration**
   - Capture images via webcam and label with a person's name
   - Store in `/known_faces/`
   - Create facial encodings and store in `encodings.pkl`

2. **Real-Time Recognition**
   - GUI captures webcam input
   - Matches face with known encodings
   - If recognized:
     - Display name
     - Send `1` via Serial to Arduino
   - Else:
     - Show "Unknown"
     - Send `0` to Arduino

3. **Servo Response**
   - Arduino receives signal
   - If `1` → Rotate Servo to simulate action
   - If `0` → Do nothing

---

## 🔌 Hardware Circuit (Servo Motor + Arduino UNO)

**Connections:**
| Servo Wire | Arduino Pin |
|------------|-------------|
| Orange (Signal) | D9          |
| Red (VCC)       | 5V          |
| Brown (GND)     | GND         |

**Serial Baud Rate:** `9600`

---

## 🧪 How to Run

### 1️⃣ Requirements

Install [Anaconda](https://www.anaconda.com/) (recommended) or ensure Python ≥ 3.8.

### 2️⃣ Create a Virtual Environment

```bash
conda create -n face_robot python=3.8
conda activate face_robot
3️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Upload Arduino Code
Open arduino_control.ino in Arduino IDE

Connect Arduino Uno

Upload code

5️⃣ Run the GUI
bash
Copy
Edit
python gui_main.py
Use the GUI to:

Register face with name

Start recognition

Servo will respond if face is recognized

🧰 requirements.txt
opencv-python
face_recognition
Pillow
numpy
pyserial
