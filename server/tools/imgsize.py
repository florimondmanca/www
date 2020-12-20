import statistics
import sys

from .. import settings
from .utils import get_img_paths

KB = 1024


def main() -> int:
    rv = 0
    sizes = []

    for path in get_img_paths():
        size = path.stat().st_size
        sizes.append(size)
        if size / KB > settings.IMAGE_ALLOWED_MAX_SIZE_KB:  # pragma: no cover
            print(
                f"ERROR: image is too big "
                f"({size / KB:.2f}kB > {settings.IMAGE_ALLOWED_MAX_SIZE_KB}kB): {path}"
            )
            rv |= 1

    if sizes:
        print(
            f"sizes: ("
            f"min: {min(sizes) / KB:.2f}kB, "
            f"max: {max(sizes) / KB:.2f}kB, "
            f"avg: {statistics.mean(sizes) / KB:.2f}kB, "
            f"mdn: {statistics.median(sizes) / KB:.2f}kB, "
            f"std: {statistics.stdev(sizes) / KB:.2f}kB"
            ")"
        )

    return rv


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
