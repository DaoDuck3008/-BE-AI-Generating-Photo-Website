from PIL import Image

SIZE_MAP = {
    "3x4 cm": (354, 472),
    "4x6 cm": (472, 709),
    "2x2 inch": (600, 600),
}

class ResizeError(Exception):
    pass

def crop_object_cover(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    src_w, src_h = img.size
    src_ratio = src_w / src_h
    target_ratio = target_w / target_h

    if src_ratio > target_ratio:
        # Ảnh quá rộng → cắt ngang
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        box = (left, 0, left + new_w, src_h)
    else:
        # Ảnh quá cao → cắt dọc
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        box = (0, top, src_w, top + new_h)

    return img.crop(box)


def resize_image (img: Image.Image, size: str) -> Image.Image:
    if size not in SIZE_MAP:
        raise ResizeError("Unsupported size")

    target_w , target_h = SIZE_MAP[size]

    img = crop_object_cover(img, target_w, target_h)

    return img.resize(
        (target_w, target_h),
        resample= Image.Resampling.LANCZOS
    )