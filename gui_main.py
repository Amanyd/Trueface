import csv
import serial
import os
import pickle
import datetime
from tkinter import simpledialog, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import cv2

# Set the path to local face recognition models
os.environ['FACE_RECOGNITION_MODELS'] = os.path.join(os.getcwd(), 'models', 'face_recognition_models')

import face_recognition

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Create main window
window = ctk.CTk()
window.title("TrueFace - Face Recognition System")
window.geometry("1000x800")
window.configure(fg_color="#0a0a0a")

# Main container
main_frame = ctk.CTkFrame(window, fg_color="#111111", corner_radius=12)
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Header
header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
header_frame.pack(fill="x", padx=20, pady=(20, 10))

title_label = ctk.CTkLabel(header_frame, text="TrueFace Recognition", 
                          font=ctk.CTkFont(size=24, weight="bold"),
                          text_color="#ffffff")
title_label.pack(side="left")

status_label = ctk.CTkLabel(header_frame, text="● Ready", 
                           font=ctk.CTkFont(size=14),
                           text_color="#10b981")
status_label.pack(side="right")

# Video container
video_container = ctk.CTkFrame(main_frame, fg_color="#1a1a1a", corner_radius=8)
video_container.pack(fill="x", padx=20, pady=10)

video_label = ctk.CTkLabel(video_container, text="")
video_label.pack(pady=20)

# Global webcam variable with optimized settings
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# Ensure images directory exists
if not os.path.exists("images"):
    os.makedirs("images")

# Controls section
controls_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
controls_frame.pack(fill="x", padx=20, pady=10)

# User dropdown section
user_section = ctk.CTkFrame(controls_frame, fg_color="#1a1a1a", corner_radius=8)
user_section.pack(fill="x", pady=(0, 15))

user_label = ctk.CTkLabel(user_section, text="Registered Users", 
                         font=ctk.CTkFont(size=14, weight="bold"),
                         text_color="#e5e5e5")
user_label.pack(pady=(15, 5))

user_list = ctk.StringVar()
user_dropdown = ctk.CTkComboBox(user_section, variable=user_list, state="readonly",
                               width=300, height=35,
                               fg_color="#2a2a2a", border_color="#404040",
                               button_color="#404040", button_hover_color="#505050",
                               values=["No users registered"])
user_dropdown.set("No users registered")
user_dropdown.pack(pady=(0, 15))

def update_user_dropdown():
    if os.path.exists("encodings.pkl"):
        with open("encodings.pkl", "rb") as f:
            _, known_names = pickle.load(f)
        unique_names = sorted(set(known_names))
        user_dropdown.configure(values=unique_names)
        if unique_names:
            user_dropdown.set(f"{len(unique_names)} users registered")
        else:
            user_dropdown.set("No users registered")
    else:
        user_dropdown.configure(values=["No users registered"])
        user_dropdown.set("No users registered")

def update_frame():
    ret, frame = cap.read()
    if ret:
        # Resize frame for bigger display
        frame = cv2.resize(frame, (640, 480))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        # Use CTkImage to fix the warning
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(640, 480))
        video_label.configure(image=ctk_img)
        video_label.image = ctk_img  # Keep a reference
    video_label.after(33, update_frame)  # ~30 FPS instead of 50 FPS

def register_face():
    name = simpledialog.askstring("Enter Name", "What is your name?")
    if not name:
        return

    existing_names = []
    if os.path.exists("encodings.pkl"):
        with open("encodings.pkl", "rb") as f:
            _, existing_names = pickle.load(f)

    same_name_count = existing_names.count(name)
    unique_name = f"{name}_{same_name_count + 1}" if same_name_count > 0 else name

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
            image_path = f"images/{unique_name}_{timestamp}_{capture_count+1}.jpg"
            cv2.imwrite(image_path, frame)
            capture_count += 1
            face_found = True

    if not face_found:
        show_custom_dialog("No Face Detected", "No valid face captured. Please try again.", "warning")
        return

    if os.path.exists("encodings.pkl"):
        with open("encodings.pkl", "rb") as f:
            known_encodings, known_names = pickle.load(f)
    else:
        known_encodings, known_names = [], []

    known_encodings.extend(encodings_to_save)
    known_names.extend([unique_name] * len(encodings_to_save))

    with open("encodings.pkl", "wb") as f:
        pickle.dump((known_encodings, known_names), f)

    update_user_dropdown()
    show_custom_dialog("Registration Complete", f"{len(encodings_to_save)} face encodings registered for {unique_name}.", "success")

def show_custom_dialog(title, message, dialog_type="info"):
    """Custom styled dialog box"""
    dialog = ctk.CTkToplevel(window)
    dialog.title(title)
    dialog.geometry("400x200")
    dialog.configure(fg_color="#111111")
    dialog.resizable(False, False)
    dialog.transient(window)
    dialog.grab_set()
    
    # Center the dialog
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
    y = (dialog.winfo_screenheight() // 2) - (200 // 2)
    dialog.geometry(f"400x200+{x}+{y}")
    
    # Content frame
    content_frame = ctk.CTkFrame(dialog, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Icon and message
    icon_colors = {"info": "#0070f3", "success": "#10b981", "error": "#dc2626", "warning": "#f59e0b"}
    icons = {"info": "ℹ", "success": "✓", "error": "✕", "warning": "⚠"}
    
    icon_label = ctk.CTkLabel(content_frame, text=icons.get(dialog_type, "ℹ"), 
                             font=ctk.CTkFont(size=24), 
                             text_color=icon_colors.get(dialog_type, "#0070f3"))
    icon_label.pack(pady=(10, 5))
    
    msg_label = ctk.CTkLabel(content_frame, text=message, 
                            font=ctk.CTkFont(size=14),
                            text_color="#e5e5e5", wraplength=350)
    msg_label.pack(pady=(0, 20))
    
    # OK button
    ok_btn = ctk.CTkButton(content_frame, text="OK", 
                          font=ctk.CTkFont(size=12, weight="bold"),
                          command=dialog.destroy, width=100, height=35,
                          fg_color=icon_colors.get(dialog_type, "#0070f3"),
                          corner_radius=6)
    ok_btn.pack()
    
    dialog.wait_window()

def recognize_face():
    if not os.path.exists("encodings.pkl"):
        show_custom_dialog("Error", "No faces registered yet.", "error")
        return

    with open("encodings.pkl", "rb") as f:
        known_encodings, known_names = pickle.load(f)

    try:
        arduino = serial.Serial('COM4', 9600, timeout=1)
        robot_connected = True
    except:
        robot_connected = False
        print("⚠️ Arduino not connected. Running in face-only mode.")

    show_custom_dialog("Recognition Started", "Press Q in the video window to stop recognition.", "info")
    
    # Update status
    status_label.configure(text="● Recognizing", text_color="#f59e0b")
    window.update()

    # Performance optimization variables
    frame_count = 0
    process_every_n_frames = 3  # Process every 3rd frame for better performance
    last_known_faces = []  # Cache last known face locations

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame_count += 1
        
        # Only process face recognition every N frames to reduce lag
        if frame_count % process_every_n_frames == 0:
            # Resize frame for faster processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")  # Use HOG model for speed
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            
            # Scale back up face locations since frame was scaled down
            face_locations = [(top*2, right*2, bottom*2, left*2) for (top, right, bottom, left) in face_locations]
            
            # Update cache
            last_known_faces = []
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                distances = face_recognition.face_distance(known_encodings, face_encoding)
                best_match_index = distances.argmin() if len(distances) else None
                name = "Unknown"

                if best_match_index is not None and distances[best_match_index] < 0.5:
                    name = known_names[best_match_index]

                last_known_faces.append(((top, right, bottom, left), name))

                if robot_connected:
                    if name != "Unknown":
                       arduino.write(b'1\n')  # recognized → move servo
                    else:
                           arduino.write(b'0\n')  # unrecognized → do nothing

                with open("logs.csv", "a", newline="") as logfile:
                        writer = csv.writer(logfile)
                        writer.writerow([name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        
        # Draw rectangles and names using cached data (every frame for smooth display)
        for (top, right, bottom, left), name in last_known_faces:
            color = (0, 255, 0) if name != "Unknown" else (255, 100, 100)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            # Better text styling
            label_size = cv2.getTextSize(name, cv2.FONT_HERSHEY_DUPLEX, 0.7, 2)[0]
            cv2.rectangle(frame, (left, top - 30), (left + label_size[0] + 8, top), color, -1)
            cv2.putText(frame, name, (left + 4, top - 8), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("TrueFace Recognition - Press Q to Quit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    status_label.configure(text="● Ready", text_color="#10b981")
    window.update()

def clear_all_data():
    if os.path.exists("encodings.pkl"):
        os.remove("encodings.pkl")
    if os.path.exists("logs.csv"):
        os.remove("logs.csv")
    for file in os.listdir("images"):
        os.remove(os.path.join("images", file))
    update_user_dropdown()
    show_custom_dialog("Data Cleared", "All registered data has been deleted.", "success")

# Action buttons - centered horizontally
btn_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
btn_frame.pack(expand=True)

# Create inner frame for centering
btn_inner_frame = ctk.CTkFrame(btn_frame, fg_color="transparent")
btn_inner_frame.pack()

register_btn = ctk.CTkButton(btn_inner_frame, text="Register New Face", 
                            font=ctk.CTkFont(size=14, weight="bold"),
                            command=register_face, width=200, height=45,
                            fg_color="#0070f3", hover_color="#0051cc",
                            corner_radius=8)
register_btn.grid(row=0, column=0, padx=(0, 15))

recognize_btn = ctk.CTkButton(btn_inner_frame, text="Start Recognition", 
                             font=ctk.CTkFont(size=14, weight="bold"),
                             command=recognize_face, width=200, height=45,
                             fg_color="#10b981", hover_color="#059669",
                             corner_radius=8)
recognize_btn.grid(row=0, column=1, padx=(0, 15))

clear_btn = ctk.CTkButton(btn_inner_frame, text="Clear All Data", 
                         font=ctk.CTkFont(size=14, weight="bold"),
                         command=clear_all_data, width=200, height=45,
                         fg_color="#dc2626", hover_color="#b91c1c",
                         corner_radius=8)
clear_btn.grid(row=0, column=2)

update_user_dropdown()
update_frame()
window.mainloop()
 
cap.release()
cv2.destroyAllWindows()