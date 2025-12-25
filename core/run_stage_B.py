from PIL import Image
from io import BytesIO
import requests

from core.stage_B import validate_cloudinary_url, adjust_color_image, add_background_color, resize_image

def run_stage_B (
        img_path: str,
        bg_color: str,
        size: str,
        brightness: int,
        contrast: int,
        saturation: int,
        print_form: str
        ):
    # Kiểm tra xem ảnh có đúng là đến từ cloudinary không? 
    validate_cloudinary_url(img_path)

    # Lấy hình ảnh từ img_path do Frontend gửi về trước
    response = requests.get(img_path, timeout=10)
    response.raise_for_status()  # lỗi nếu 4xx / 5xx

    # Lưu tạm vào BytesIO rồi mở ảnh bằng Pillow
    img_bytes = BytesIO(response.content)
    img  = Image.open(img_bytes).convert("RGBA") 
    # Điều chỉnh màu
    rgb_img = img.convert("RGB")
    adjusted_rgb = adjust_color_image(rgb_img,brightness,contrast,saturation)
    
    # Convert về RGBA
    adjusted_rgba = adjusted_rgb.convert("RGBA")
    adjusted_rgba.putalpha(img.split()[3]) # điền lại alpha gốc 

    # Thay màu nền theo yêu cầu
    bg_img = add_background_color(adjusted_rgba, bg_color)

    # Resize ảnh đúng chuẩn DPI 300
    final_img = resize_image(bg_img, size)
    final_img.show()

    return