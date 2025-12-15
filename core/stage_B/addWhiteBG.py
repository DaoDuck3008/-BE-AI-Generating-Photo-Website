from PIL import Image

def add_white_background(image, output_path):
    img = image.convert("RGBA")
    white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    white_bg.paste(img, (0, 0), img)
    white_bg.convert("RGB").save(output_path, "JPEG")
    print(f"✅ White background added and image saved as {output_path}")