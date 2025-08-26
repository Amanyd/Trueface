import cv2
import os
import pickle

# Set the path to local face recognition models
os.environ['FACE_RECOGNITION_MODELS'] = os.path.join(os.getcwd(), 'models', 'face_recognition_models')

import face_recognition
import cv2

known_faces = []
known_names = []

name = input("Enter name: ")

cap = cv2.VideoCapture(0)
print("📸 Press 's' to capture and save face. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    cv2.imshow("Register Face", frame)

    key = cv2.waitKey(1)

    if key == ord('s'):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, boxes)

        if encodings:
            known_faces.append(encodings[0])
            known_names.append(name)
            print("✅ Face captured and encoded")
        else:
            print("⚠️ No face found. Try again.")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

with open("encodings.pkl", "wb") as f:
    pickle.dump((known_faces, known_names), f)
print("🧠 Saved encodings.pkl")
