from urllib.parse import urlparse

class ValidateError(Exception):
    pass

def validate_cloudinary_url(url: str):
    if not isinstance(url, str):
        raise ValidateError("Image URL must be a string")

    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise ValidateError("Invalid URL scheme")

    if "res.cloudinary.com" not in parsed.netloc:
        raise ValidateError("Invalid Cloudinary domain")

    return True
