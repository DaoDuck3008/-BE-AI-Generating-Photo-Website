from config import INPUT_DIR, OUTPUT_DIR
from core.stage_A.background_removal import remove_background
from core.stage_B.addWhiteBG import add_white_background


INPUT_IMAGE = INPUT_DIR / "sample1.jpg"
OUTPUT_IMAGE = OUTPUT_DIR / "sample1_no_bg.png"

# Bước A2: Xóa nền
refined_image = remove_background(image_path=INPUT_IMAGE)

# Bước B2: Thêm nền trắng
add_white_background(refined_image, OUTPUT_IMAGE)