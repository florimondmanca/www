from urllib.parse import urlencode

from . import settings

# See: https://unsplash.com/documentation#dynamically-resizable-images


def make_image(photo_id: str) -> str:
    queryparams = {
        "auto": "format",
        "fit": "crop",
        "w": settings.UNSPLASH_IMAGE_WIDTH,
        "q": settings.UNSPLASH_IMAGE_QUALITY,
    }
    query = urlencode(queryparams)
    return f"https://images.unsplash.com/{photo_id}?{query}"


def make_image_thumbnail(photo_id: str) -> str:
    queryparams = {
        "auto": "format",
        "fit": "crop",
        "w": settings.UNSPLASH_IMAGE_THUMBNAIL_WIDTH,
        "q": settings.UNSPLASH_IMAGE_THUMBNAIL_QUALITY,
    }
    query = urlencode(queryparams)
    return f"https://images.unsplash.com/{photo_id}?{query}"
