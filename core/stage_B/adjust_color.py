from PIL import Image, ImageEnhance

class AdjustColorError(Exception):
    pass

def adjust_color_image (img: Image.Image,brightness: int = 100, contrast: int = 100, saturation: int = 100):
    if brightness < 0 or brightness > 200:
        raise AdjustColorError(f"brightness {brightness} is not allowed!")
    
    if contrast < 0 or contrast > 200:
        raise AdjustColorError(f"Contrast {contrast} is not allowed!")
    
    if saturation < 0 or saturation > 200:
        raise AdjustColorError(f"Saturation {saturation} is not allowed!")

    # Convert % -> hệ số
    brightness_factor = brightness / 100
    contrast_factor = contrast / 100
    saturation_factor = saturation / 100
    
    # Điều chỉnh độ sáng (Brightness)
    if brightness != 100:
        img  =ImageEnhance.Brightness(img).enhance(brightness_factor)

    # Điều chỉnh độ tương phản (Contrast)
    if contrast != 100:
        img = ImageEnhance.Contrast(img).enhance(contrast_factor)

    # Điều chỉnh độ bão hòa (Saturation)
        img = ImageEnhance.Color(img).enhance(saturation_factor)

    return img