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
window.title("Face Recognition Robot Interface 🤖")
window.geometry("800x600")
window.configure(bg="#1e1e1e")

# Webcam Frame
video_label = tk.Label(window)
video_label.pack(pady=10)

# Global webcam variable
cap = cv2.VideoCapture(0)

def update_frame():
    ret, frame = cap.read()
    if ret:
        # Convert frame to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

    # Repeat every 20 ms
    video_label.after(20, update_frame)

# Placeholder functions
def register_face():
    # Prompt for name
    name = simpledialog.askstring("Enter Name", "What is your name?")
    if not name:
        return

    ret, frame = cap.read()
    if not ret:
        messagebox.showerror("Error", "Failed to capture image.")
        return

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    if len(encodings) == 0:
        messagebox.showwarning("No Face", "No face detected. Try again.")
        return

    encoding = encodings[0]

    # Save to encodings.pkl
    if os.path.exists("encodings.pkl"):
        with open("encodings.pkl", "rb") as f:
            known_encodings, known_names = pickle.load(f)
    else:
        known_encodings, known_names = [], []

    known_encodings.append(encoding)
    known_names.append(name)

    with open("encodings.pkl", "wb") as f:
        pickle.dump((known_encodings, known_names), f)

    # Save image
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = f"images/{name}_{timestamp}.jpg"
    cv2.imwrite(image_path, frame)

    messagebox.showinfo("Success", f"Face registered for {name}.")

def recognize_face():
    if not os.path.exists("encodings.pkl"):
        messagebox.showerror("Error", "No faces registered yet.")
        return

    # Load known encodings
    with open("encodings.pkl", "rb") as f:
        known_encodings, known_names = pickle.load(f)

    # Setup serial 
    try:
        arduino = serial.Serial('COM3', 9600, timeout=1)  # Change COM3 as needed
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
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                match_index = matches.index(True)
                name = known_names[match_index]

                # Send to Arduino
                if robot_connected:
                    arduino.write((name + "\n").encode())

                # Log to CSV
                with open("logs.csv", "a", newline="") as logfile:
                    writer = csv.writer(logfile)
                    writer.writerow([name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

            # Draw box + name
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        # Show updated frame
        cv2.imshow("Recognizing Faces - Press Q to Quit", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

# Buttons
btn_frame = tk.Frame(window, bg="#1e1e1e")
btn_frame.pack(pady=20)

register_btn = tk.Button(btn_frame, text="Register Face", font=("Arial", 14), command=register_face, bg="#3498db", fg="white", width=20)
register_btn.grid(row=0, column=0, padx=20)

recognize_btn = tk.Button(btn_frame, text="Start Recognition", font=("Arial", 14), command=recognize_face, bg="#2ecc71", fg="white", width=20)
recognize_btn.grid(row=0, column=1, padx=20)

# Start the video stream
update_frame()

# Main loop
window.mainloop()

# Release resources
cap.release()
cv2.destroyAllWindows()
