"""
Optimize the size of images.

Currently this merely reduces the number of unique colors
"""
import argparse
import statistics
import sys
import tempfile
from pathlib import Path

from PIL import Image

from . import imgsize
from .utils import get_img_paths

KB = 1024


def _main_check() -> int:
    rv = 0

    for path_in in get_img_paths():
        # Our conversion method requires using PNG.
        path_out = path_in.with_name(f"{path_in.stem}.png")

        im = Image.open(path_in)
        size_actual = path_in.stat().st_size

        if path_in.suffix != ".png":
            # Ignore JPG -- they can't possibly come from this script.
            continue

        with tempfile.TemporaryDirectory() as tmpdir:
            outim = im.convert("P", colors=32)
            path_out = Path(tmpdir) / path_out.name
            outim.save(path_out)
            size_expected = path_out.stat().st_size

        if size_actual != size_expected:  # pragma: no cover
            print(f"ERROR: image could be optimized: {path_in}")
            rv |= 1

    if rv:  # pragma: no cover
        print(
            "Some images could be optimized. "
            "Run `python -m server.tools.imgoptimize` to fix."
        )
    return rv


def _main() -> int:  # pragma: no cover
    converted = 0
    skipped = 0
    size_reductions = []
    sizes = []
    rv = 0

    for path_in in get_img_paths():
        # Our conversion method requires using PNG.
        path_out = path_in.with_name(f"{path_in.stem}.png")

        im_initial = Image.open(path_in)
        size_initial = path_in.stat().st_size
        im = im_initial

        if path_in.suffix == ".jpg":
            # PNG is typically larger than JPG (especially for photo-realistic images),
            # but let's try.
            im.save(path_out)
            im = Image.open(path_out)

        # Reduce maximum number of unique colors, which should reduce
        # image size a fair bit.
        outim = im.convert("P", colors=32)
        outim.save(path_out)
        size_final = path_out.stat().st_size

        if size_final > size_initial:
            print(f"skipped: would increase filesize: {path_in}")
            path_out.unlink()
            sizes.append(size_initial)
            skipped += 1
            continue

        if path_in.suffix == ".jpg":
            path_in.unlink()

        size_reduction = (size_final - size_initial) / size_initial
        if size_reduction != 0:
            print(
                f"converted: {path_in}: "
                f"{size_initial / KB:.2f}kB -> {size_final / KB:.2f}kB "
                f"({size_reduction * 100:.2f}%)"
            )
        size_reductions.append(-size_reduction)
        sizes.append(size_final)

        converted += 1

    assert converted == len(size_reductions)
    print(f"{converted} images converted, {skipped} images skipped")

    if size_reductions:
        print(
            f"size reduction: ("
            f"min: -{min(size_reductions) * 100:.2f}%, "
            f"max: {-max(size_reductions) * 100:.2f}%, "
            f"avg: -{statistics.mean(size_reductions) * 100:.2f}%"
            ")"
        )

    rv |= imgsize.main()

    return rv


def main(check: bool) -> int:
    if check:
        return _main_check()
    else:  # pragma: no cover
        return _main()


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    sys.exit(main(check=args.check))
