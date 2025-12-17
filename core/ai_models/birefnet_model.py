import torch
from models.birefnet import BiRefNet

MODEL_NAME = "zhengpeng7/BiRefNet-portrait"

device = "cuda" if torch.cuda.is_available() else "cpu"

print("🔄 Loading BiRefNet model...")

birefnet = BiRefNet.from_pretrained(MODEL_NAME)
birefnet.to(device)
birefnet.eval()

torch.set_float32_matmul_precision("high")

print(f"✅ BiRefNet loaded on {device}")
