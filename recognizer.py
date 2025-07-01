import cv2
import face_recognition
import pickle
import serial
import time
import csv
from datetime import datetime
import os

# === Arduino Setup ===
try:
    arduino = serial.Serial('COM3', 9600)  # Change COM port as per your system
    time.sleep(2)  # Wait for Arduino to initialize
except:
    arduino = None
    print("⚠️ Arduino not connected. Face recognition will run without robot action.")

# === Load Known Encodings ===
with open('encodings.pkl', 'rb') as f:
    known_encodings, known_names = pickle.load(f)

# === CSV Log Setup ===
if not os.path.exists('logs.csv'):
    with open('logs.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Time'])

def log_recognition(name):
    with open('logs.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

# === Start Webcam ===
cap = cv2.VideoCapture(0)
print("📷 Press 'q' to quit")

while True:
    ret, frame = cap.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.45)
        name = "Unknown"

        if True in matches:
            index = matches.index(True)
            name = known_names[index]

            # Draw box
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            log_recognition(name)

            if arduino:
                arduino.write(name.encode())  # Send name to Arduino
                print(f"📤 Sent to Arduino: {name}")

        else:
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    cv2.imshow('Face Recognition', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
