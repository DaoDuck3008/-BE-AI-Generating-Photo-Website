import numpy as np
from PIL import Image
import cv2
from utilities import get_nose_and_chin_from_pil

def align_and_crop_image(
        image_rgba: Image.Image,
        chin_margin_ratio: float = 0.4 # phần trăm khoảng cách từ mũi đến cằm để thêm vào vùng cằm
) -> Image.Image:
    """
    Input:
        image_rgba: PIL.Image (RGBA)
        chin_margin_ratio: float, phần trăm khoảng cách từ mũi đến cằm để thêm vào vùng cằm
    Output:
        cropped_aligned_image: PIL.Image (RGBA)
    """

    # 1. Chuẩn bị ảnh
    img = np.array(image_rgba) # PIL -> NumPy array
    h, w = img.shape[:2]

    (nose_x, nose_y), (chin_x, chin_y) = get_nose_and_chin_from_pil(image_rgba) # Lấy tọa độ mũi và cằm


    # 2. Xacs định target position
    target_nose_x = w // 2 # Vị trí mũi mục tiêu (giữa ảnh)
    target_chin_y = h * (1 - chin_margin_ratio) # Vị trí cằm mục tiêu

    dx = target_nose_x - nose_x
    dy = target_chin_y - chin_y

    # 3. Dịch toàn bộ ảnh RGBA
    M = np.float32([[1, 0, dx],
                    [0, 1, dy]]) # Ma trận dịch chuyển
    
    shifted = cv2.warpAffine(img, M, (w, h),
                            flags= cv2.INTER_LINEAR,
                            borderMode=cv2.BORDER_CONSTANT, 
                            borderValue=(0,0,0,0)) # Dịch ảnh với nền trong suốt
    
    # 4. Crop ảnh
    target_ratio = 2/3
    current_ratio = w / h

    if current_ratio > target_ratio:
        # Ảnh quá rộng, cần crop bớt chiều rộng
        new_w = int(h * target_ratio)
        x_start = int((w - new_w) // 2)
        cropped = shifted[:, x_start:x_start + new_w]

    elif current_ratio < target_ratio:
        # Ảnh quá cao, cần crop bớt chiều cao
        new_h = int(w / target_ratio)
        y_start = int(h - new_h)
        cropped = shifted[y_start:y_start + new_h, :]

    else:
        # Tỉ lệ đã đúng
        cropped = shifted

    print("✅ Stage A3 - Image aligned and cropped.")
    
    return Image.fromarray(cropped, mode="RGBA")