from PIL import Image

def add_background_color(image_rgba: Image.Image, bg_color:str = "#0d93d1"):
    background = Image.new("RGB", image_rgba.size, bg_color)
    background.paste(
        image_rgba,
        mask = image_rgba.split()[3]    
    )

    return background