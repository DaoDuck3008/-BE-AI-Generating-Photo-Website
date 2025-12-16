import cv2 
import numpy as np
from PIL import Image
import mediapipe as mp

mp_face = mp.solutions.face_mesh

def get_nose_and_chin_from_pil(image_rgba: Image.Image) -> tuple:
    """
    Input:
        image_rgba: PIL.Image (RGBA)
    Output:
        nose_xy: (x, y) pixel
        chin_xy: (x, y) pixel
    """

    # 1. PIL GRBA -> RGB -> NumPy array
    # Vì MediaPipe Face Mesh yêu cầu ảnh đầu vào là RGB, nso không hiểu alpha
    image_rgb = image_rgba.convert("RGB")
    img_np = np.array(image_rgb)

    h, w = img_np.shape[:2] # lấy height, width
    

    # 2. Sử dụng MediaPipe Face Mesh để phát hiện mặt và các điểm đặc trưng
    with mp_face.FaceMesh(static_image_mode=True, 
                          max_num_faces=1, 
                          refine_landmarks= True, 
                          min_detection_confidence = 0.5) as face_mesh:
        results = face_mesh.process(img_np)

        if not results.multi_face_landmarks:
            raise ValueError("No face detected in the image.")
        
        landmarks = results.multi_face_landmarks[0].landmark # Lấy landmarks của khuôn mặt đầu tiên

        # 3. Lấy tọa độ điểm mũi và cằm
        nose_landmark = landmarks[1]
        chin_landmark = landmarks[152]

        # 4. chuyeenr sang pixel
        nose_x = int(nose_landmark.x * w)
        nose_y = int(nose_landmark.y * h)

        chin_x = int(chin_landmark.x * w)
        chin_y = int(chin_landmark.y * h)

        return (nose_x, nose_y), (chin_x, chin_y)