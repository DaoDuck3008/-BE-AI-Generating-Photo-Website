from PIL import Image

def add_white_background(image):
    img = image.convert("RGBA")
    white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    white_bg.paste(img, (0, 0), img)
    return white_bg.convert("RGB")