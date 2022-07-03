from pathlib import Path
from typing import List


def get_img_paths() -> List[Path]:
    patterns = [
        "server/**/static/img/**/*.png",
        "server/**/static/img/**/*.jpg",
    ]
    return [path for pattern in patterns for path in Path().glob(pattern)]
