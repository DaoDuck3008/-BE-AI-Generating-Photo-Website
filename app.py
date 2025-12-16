from config import INPUT_DIR, OUTPUT_DIR
from core.stage_A import remove_background, align_and_crop_image
from core.stage_B import add_white_background


INPUT_IMAGE = INPUT_DIR / "sample6.jpg"
OUTPUT_IMAGE = OUTPUT_DIR / "sample1_no_bg.png"

# Bước A2: Xóa nền
refined_image = remove_background(image_path=INPUT_IMAGE)

# Bước A3: căn chỉnh người và crop theo tỉ lệ 2/3
new_image = align_and_crop_image(refined_image)

# Bước A4: Chèn nền mới (nếu cần)
new_image = add_white_background(new_image)

new_image.show()
new_image.save(OUTPUT_IMAGE)