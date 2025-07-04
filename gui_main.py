import csv
import serial
import face_recognition
import pickle
import os
import datetime
from tkinter import simpledialog
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2

# Create main window
window = tk.Tk()
window.title("Face Recognition Robot Interface \U0001F916")
window.geometry("800x600")
window.configure(bg="#1e1e1e")

# Webcam Frame
video_label = tk.Label(window)
video_label.pack(pady=10)

# Global webcam variable
cap = cv2.VideoCapture(0)

# Ensure images directory exists
if not os.path.exists("images"):
    os.makedirs("images")

def update_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    video_label.after(20, update_frame)

def register_face():
    name = simpledialog.askstring("Enter Name", "What is your name?")
    if not name:
        return

    face_found = False
    encodings_to_save = []
    capture_count = 0

    while capture_count < 5:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if len(encodings) == 1:
            encodings_to_save.append(encodings[0])
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = f"images/{name}_{timestamp}_{capture_count+1}.jpg"
            cv2.imwrite(image_path, frame)
            capture_count += 1
            face_found = True

    if not face_found:
        messagebox.showwarning("No Face", "No valid face captured. Try again.")
        return

    if os.path.exists("encodings.pkl"):
        with open("encodings.pkl", "rb") as f:
            known_encodings, known_names = pickle.load(f)
    else:
        known_encodings, known_names = [], []

    known_encodings.extend(encodings_to_save)
    known_names.extend([name] * len(encodings_to_save))

    with open("encodings.pkl", "wb") as f:
        pickle.dump((known_encodings, known_names), f)

    messagebox.showinfo("Success", f"{len(encodings_to_save)} face encodings registered for {name}.")

def recognize_face():
    if not os.path.exists("encodings.pkl"):
        messagebox.showerror("Error", "No faces registered yet.")
        return

    with open("encodings.pkl", "rb") as f:
        known_encodings, known_names = pickle.load(f)

    try:
        arduino = serial.Serial('COM3', 9600, timeout=1)
        robot_connected = True
    except:
        robot_connected = False
        print("⚠️ Arduino not connected. Running in face-only mode.")

    messagebox.showinfo("Recognition Started", "Press Q in the video window to stop.")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = distances.argmin() if len(distances) else None
            name = "Unknown"

            if best_match_index is not None and distances[best_match_index] < 0.5:
                name = known_names[best_match_index]

                if robot_connected:
                    arduino.write((name + "\n").encode())

                with open("logs.csv", "a", newline="") as logfile:
                    writer = csv.writer(logfile)
                    writer.writerow([name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        cv2.imshow("Recognizing Faces - Press Q to Quit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

btn_frame = tk.Frame(window, bg="#1e1e1e")
btn_frame.pack(pady=20)

register_btn = tk.Button(btn_frame, text="Register Face", font=("Arial", 14), command=register_face, bg="#3498db", fg="white", width=20)
register_btn.grid(row=0, column=0, padx=20)

recognize_btn = tk.Button(btn_frame, text="Start Recognition", font=("Arial", 14), command=recognize_face, bg="#2ecc71", fg="white", width=20)
recognize_btn.grid(row=0, column=1, padx=20)

update_frame()
window.mainloop()

cap.release()
cv2.destroyAllWindows()
