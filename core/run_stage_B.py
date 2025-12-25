from PIL import Image
from io import BytesIO
import requests

from core.stage_B.validate_cloud_url import validate_cloudinary_url, ValidateError
from core.stage_B.adjust_color import adjust_color_image, AdjustColorError
from core.stage_B.add_background import add_background_color
from core.stage_B.resize_img import resize_image, ResizeError
from core.stage_B.add_layout import layout_4R, LayoutError
from core.save_img import save_img, SaveImageError

class StageBError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)

def run_stage_B (
        img_path: str,
        bg_color: str,
        size: str,
        brightness: int,
        contrast: int,
        saturation: int,
        print_form: bool
        ):
    try:
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

        # đưa ảnh vào khung in 
        if(print_form):
            canvas = layout_4R(final_img, size)        
        else:
            canvas = final_img
        
        # Lưu ảnh lên cloud
        result = save_img(image=canvas, folder="potrait_photos", format="PNG")

        return result["secure_url"]
    
    except ValidateError as e:
        raise StageBError(
            code="VALIDATE_FAILED",
            message= str(e)
        )
    
    except AdjustColorError as e:
        raise StageBError(
            code="ADJUST_COLOR_FAILED",
            message= str(e)
        )
    
    except ResizeError as e:
        raise StageBError(
            code="RESIZE_FAILED",
            message= str(e)
        )

    except LayoutError as e:
        raise StageBError(
            code="LAYOUT_FAILED",
            message= str(e)
        )
    
    except SaveImageError as e:
        raise StageBError(
            code="SAVE_IMAGE_FAILED",
            message= str(e)
        )

    except Exception:
        raise StageBError(
            code="STAGE_B_UNKNOWN",
            message="Stage B proccessing failed."
        )