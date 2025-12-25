from PIL import Image, ImageEnhance

def adjust_color_image (img: Image.Image,brightness: int = 100, contrast: int = 100, saturation: int = 100):
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