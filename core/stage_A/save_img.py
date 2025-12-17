from PIL import Image
import os
from io import BytesIO
from dotenv import load_dotenv
import cloudinary.uploader

load_dotenv()

def save_img(image: Image.Image, folder="potrait_photos", public_id=None, format="PNG"):
    try:
        cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
        cloud_api_key = os.getenv("CLOUDINARY_API_KEY")
        cloud_api_secret = os.getenv("CLOUDINARY_API_SECRET")

        cloudinary.config(
            cloud_name=cloud_name,
            api_key=cloud_api_key,
            api_secret=cloud_api_secret
        )

        buffer = BytesIO()
        image.save(buffer, format=format)
        buffer.seek(0)

        cloudinary.uploader.upload(
            buffer,
            folder=folder,
            public_id=public_id,
            overwrite=True,
            resource_type="image"
        )

        print("✅ Stage A4 - Image uploaded to Cloudinary successfully.")

        return
    except Exception as e:
        print(f"Error uploading image: {e}")
        return 
