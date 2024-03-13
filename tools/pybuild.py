import argparse
import re
import time
from pathlib import Path

import watchfiles

IMPORT_RE = re.compile(r"^@import (?P<path>.+);")


def _parse_import(line: str) -> str | None:
    tokens = re.split(r"\s|\n", line)

    if len(tokens) < 2:
        return None

    if tokens[0] != "@import":
        return None

    pathstr = tokens[1]

    if pathstr[0] not in ("'", '"'):
        return None

    quote = pathstr[0]
    m = re.match(f"^{quote}(?P<path>[^{quote}]+){quote}", pathstr)

    if m is None:
        return None

    return m.group("path")


def _get_imports(path: Path) -> list[tuple[int, str, Path]]:
    imports = []

    for index, line in enumerate(path.read_text().splitlines(keepends=True)):
        import_path = _parse_import(line)

        if import_path is not None:
            full_path = path.parent / import_path
            imports.append((index, line, full_path))

    return imports


def _replace_imports(path: Path) -> str:
    imports = _get_imports(path)

    lines = path.read_text().splitlines(keepends=True)

    for lineno, _, full_path in imports:
        content = _replace_imports(full_path)
        lines[lineno] = content

    return "".join(lines)


def _build(input_files: list[Path], outdir: Path) -> None:
    print()
    print("Building...")
    start = time.time()

    for path in input_files:
        output = _replace_imports(path)
        outpath = outdir / path.name
        outpath.write_text(output)
        print(f"--> {outpath}")

    elapsed_ms = (time.time() - start) * 1000
    print(f"Done in {elapsed_ms:.2f} ms")
    print()


def main(input_files: list[Path], outdir: Path, watch: bool = False) -> None:
    _build(input_files, outdir)

    if watch:
        watched_files = set(input_files)
        files_to_analyze = set(input_files)

        while files_to_analyze:
            path = files_to_analyze.pop()
            for _, _, full_path in _get_imports(path):
                watched_files.add(full_path)
                files_to_analyze.add(full_path)

        for changes in watchfiles.watch(*watched_files, raise_interrupt=False):
            changed_files = [changed_path for _, changed_path in changes]
            print(f"--> Change detected in {', '.join(changed_files)}")

            _build(input_files, outdir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", nargs="+", type=Path)
    parser.add_argument(
        "--outdir",
        help="Output built assets to this directory",
        required=True,
        type=Path,
    )
    parser.add_argument(
        "--watch", help="Rebuild upon changes in source files", action="store_true"
    )
    args = parser.parse_args()

    main(args.input_file, args.outdir, watch=args.watch)
