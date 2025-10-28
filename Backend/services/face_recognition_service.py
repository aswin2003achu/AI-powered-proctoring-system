import cv2
import face_recognition
import os

DATASET_DIR = "data/faces/"

if not os.path.exists(DATASET_DIR):
    os.makedirs(DATASET_DIR)

def register_face(image_file, name):
    """Save face encoding for a new student."""
    img_path = os.path.join(DATASET_DIR, f"{name}.jpg")
    image_file.save(img_path)

    image = face_recognition.load_image_file(img_path)
    encodings = face_recognition.face_encodings(image)
    if not encodings:
        return {"status": "failed", "message": "No face detected"}

    encoding_path = os.path.join(DATASET_DIR, f"{name}.npy")
    import numpy as np
    np.save(encoding_path, encodings[0])
    return {"status": "success", "message": f"Face registered for {name}"}
