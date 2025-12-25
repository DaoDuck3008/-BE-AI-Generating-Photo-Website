from urllib.parse import urlparse

def validate_cloudinary_url(url: str):
    if not isinstance(url, str):
        raise ValueError("Image URL must be a string")

    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise ValueError("Invalid URL scheme")

    if "res.cloudinary.com" not in parsed.netloc:
        raise ValueError("Invalid Cloudinary domain")

    return True
