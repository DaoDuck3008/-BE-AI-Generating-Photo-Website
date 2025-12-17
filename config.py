from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
INPUT_DIR = ASSETS_DIR / "inputs"
OUTPUT_DIR = ASSETS_DIR / "outputs"

UPLOAD_DIR = Path("storage/uploads")