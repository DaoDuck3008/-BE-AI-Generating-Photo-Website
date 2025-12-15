import cv2
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
from pathlib import Path

import sys
sys.path.insert(0, ".")
from models.birefnet import BiRefNet
from image_proc import refine_foreground


# =============================
# CONFIG – CHỈNH Ở ĐÂY
# =============================
MODEL_NAME = "zhengpeng7/BiRefNet-portrait"
IMAGE_SIZE = 1024


# =============================
# PREPROCESS
# =============================
transform_image = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])


# =============================
# LOAD MODEL
# =============================
def load_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = BiRefNet.from_pretrained(MODEL_NAME)
    model.to(device)
    model.eval()

    torch.set_float32_matmul_precision("high")
    print(f"✅ BiRefNet loaded on {device}")
    return model, device

model, device = load_model()

# =============================
# INFERENCE SINGLE IMAGE
# =============================
def remove_background(model=model, device=device, image_path=""):
    if not image_path:
        print("❌ Please provide valid image_path and output_path.")
        return

    image = Image.open(image_path).convert("RGB")

    input_tensor = transform_image(image).unsqueeze(0).to(device)

    autocast_ctx =  torch.no_grad()

    with autocast_ctx, torch.no_grad():
        pred = model(input_tensor)

    # Lấy output cuối
    if isinstance(pred, (list, tuple)):
        pred = pred[-1]

    alpha = pred.sigmoid().cpu()[0, 0].numpy()
    alpha = np.clip(alpha, 0, 1)

    # Resize về ảnh gốc
    alpha = cv2.resize(alpha, image.size, interpolation=cv2.INTER_CUBIC)

    # Refine foreground (theo tutorial)
    alpha_pil = Image.fromarray((alpha * 255).astype(np.uint8))
    refined = refine_foreground(image, alpha_pil, r=90, device=device)
    refined.putalpha(alpha_pil)

    return refined


    

