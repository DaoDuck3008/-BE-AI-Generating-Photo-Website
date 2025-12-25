from PIL import Image

DPI = 300 # Dots per inch
CANVAS_W, CANVAS_H = 1800, 1200

MARGIN = 60 # ~ 5mm
GAP = 35 # ~ 3mm

SIZE_MAP = {
    "3x4 cm": (354, 472),
    "4x6 cm": (472, 709),
    "2x2 inch": (600, 600),
}

LAYOUTS = { 
    "3x4 cm": (2,4),
    "4x6 cm": (2,2),
    "2x2 inch": (2,2),
}

ROTATE_FOR_LAYOUT = {
    "3x4 cm": False,
    "4x6 cm": True,
    "2x2 inch": True,
}

class LayoutError(Exception):
    pass

def layout_4R (image: Image.Image, size): 
    if size not in SIZE_MAP:
        raise LayoutError("Unsupported photo type")
    
    img_w, img_h = SIZE_MAP[size]
    rows, cols = LAYOUTS[size]
    rotate = ROTATE_FOR_LAYOUT[size]

    # Tạo canvas trắng
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), "white")
    
    # Nếu ảnh 4x6 hoặc 2x2 inch thì phải xoay
    place_w, place_h = (img_h, img_w) if rotate else (img_w, img_h)

    # Tổng vùng ảnh
    total_w  = cols * place_w + (cols - 1) * GAP
    total_h = rows * place_h + (rows - 1) * GAP

    # Canh giữa trong vùng an toàn
    start_x = (CANVAS_W - total_w) // 2
    start_y  =(CANVAS_H - total_h) // 2

    for r in range(rows):
        for c in range(cols):
            x = start_x + c * (place_w + GAP)
            y = start_y + r * (place_h + GAP)
            
            if rotate: 
                img = image.rotate(90, expand= True) # xoay ngang ảnh 
                canvas.paste(img, (x,y))
            else:
                canvas.paste(image, (x,y))

    return canvas