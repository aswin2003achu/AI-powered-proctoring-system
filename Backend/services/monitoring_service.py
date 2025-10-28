import cv2
import face_recognition
import numpy as np
import os
import time

DATASET_DIR = "data/faces/"

def monitor_exam():
    """Live camera feed for detecting multiple or unknown faces."""
    cap = cv2.VideoCapture(0)
    known_faces = []
    names = []

    for file in os.listdir(DATASET_DIR):
        if file.endswith(".npy"):
            known_faces.append(np.load(os.path.join(DATASET_DIR, file)))
            names.append(file.split(".")[0])

    start = time.time()
    alert = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = frame[:, :, ::-1]
        locations = face_recognition.face_locations(rgb_frame)
        encodings = face_recognition.face_encodings(rgb_frame, locations)

        for encoding in encodings:
            matches = face_recognition.compare_faces(known_faces, encoding, tolerance=0.6)
            if True not in matches:
                alert = "Unknown face detected!"
                break

        if len(locations) > 1:
            alert = "Multiple faces detected!"
            break

        if time.time() - start > 10:  # 10s scan period
            break

    cap.release()
    if alert:
        return alert
    else:
        return "No suspicious activity detected"
