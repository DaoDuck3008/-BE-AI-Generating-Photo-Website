import cv2
import numpy as np
from PIL import Image
from torchvision import transforms
import torch

from core.ai_models.birefnet_model import birefnet, device
from image_proc import refine_foreground

IMAGE_SIZE = 1024

transform_image = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])


def remove_background(rgb_img: Image.Image):
    print("🔍 Stage A2 - Removing background...")

    if not rgb_img:
        raise ValueError("Invalid image_path")

    input_tensor = transform_image(rgb_img).unsqueeze(0).to(device)

    with torch.no_grad():
        pred = birefnet(input_tensor)

    if isinstance(pred, (list, tuple)):
        pred = pred[-1]

    alpha = pred.sigmoid().cpu()[0, 0].numpy()
    alpha = np.clip(alpha, 0, 1)

    alpha = cv2.resize(alpha, rgb_img.size, interpolation=cv2.INTER_CUBIC)

    alpha_pil = Image.fromarray((alpha * 255).astype(np.uint8))
    refined = refine_foreground(rgb_img, alpha_pil, r=90, device=device)
    refined.putalpha(alpha_pil)

    print("✅ Stage A2 - Background removed.")
    return refined
