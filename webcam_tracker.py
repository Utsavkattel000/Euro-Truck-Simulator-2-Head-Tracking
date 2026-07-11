import cv2
import mediapipe as mp
import socket
import struct
import os
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import (
    FaceLandmarker,
    FaceLandmarkerOptions,
    RunningMode,
)
# Verify the model file exists locally
model_path = os.path.expanduser("~/Downloads/eyetracking/face_landmarker.task")
if not os.path.exists(model_path):
    print(f"Error: Could not find model asset at {model_path}. Please download it first.")
    exit(1)
# OpenTrack UDP Setup
UDP_IP = "127.0.0.1"
UDP_PORT = 4242
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=RunningMode.VIDEO,
    output_face_blendshapes=False,
    output_facial_transformation_matrixes=False,
)
cap = cv2.VideoCapture(0)
print("Webcam tracker running via MediaPipe Tasks. Press 'q' to exit.")
with FaceLandmarker.create_from_options(options) as landmarker:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        timestamp_ms = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)
        result = landmarker.detect_for_video(mp_image, timestamp_ms)
        if result.face_landmarks:
            nose = result.face_landmarks[0][1]
            x = (nose.x - 0.5) * 200  # Yaw
            y = (0.5 - nose.y) * 200  # Pitch
            data = struct.pack("dddddd", 0.0, 0.0, 0.0, x, y, 0.0)
            sock.sendto(data, (UDP_IP, UDP_PORT))
        cv2.imshow('Webcam Head Tracking', frame)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
