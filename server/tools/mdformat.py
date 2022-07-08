"""
Format ```python``` code blocks in Markdown source files:

* Apply `black`.
"""
import argparse
import io
import sys
import traceback
from pathlib import Path

import black
from pytest_codeblocks.main import extract_from_buffer

from server.infrastructure.filesystem import iter_content_paths


def _warn(text: str) -> str:
    return f"\033[93m{text}\033[0m"


def _danger(text: str) -> str:
    return f"\033[91m{text}\033[0m"


def _format_path(path: Path, *, check: bool) -> tuple[str, bool, list]:
    content = path.read_text("utf-8")
    lines = content.splitlines()
    errors = []
    offset = 0
    changed = False

    with path.open() as f:
        codeblocks = extract_from_buffer(f)

    for codeblock in codeblocks:
        if codeblock.syntax != "python":
            continue

        if "pytest.mark.skip" in codeblock.marks:
            continue

        source = codeblock.code
        lineno = codeblock.lineno
        sourcelines = source.splitlines()

        try:
            outputlines = black.format_str(
                source,
                mode=black.FileMode(target_versions={black.TargetVersion.PY37}),
            ).splitlines()
        except black.InvalidInput:
            if source.startswith(">>> "):
                # Probably a Python shell snippet. Skip it since Black can't read those.
                continue

            s = io.StringIO()
            traceback.print_exc(file=s)
            errors.append(_danger(f"ERROR: at {path}:{lineno}:\n{s.getvalue()}"))
            continue

        if sourcelines == outputlines:
            continue

        changed = True

        if check:
            continue

        lines_before = lines[: lineno + offset]
        lines_after = lines[lineno + offset + len(sourcelines) :]
        lines = lines_before + outputlines + lines_after

        offset += len(outputlines) - len(sourcelines)

    if check and changed:
        errors.append(_warn(f"Needs formatting: {path}"))

    lines.append("")  # Final newline.
    if not content.endswith("\n"):
        changed = True

    output = "\n".join(lines)

    return output, changed, errors


def _format_file(path: Path, *, check: bool) -> int:
    output, changed, errors = _format_path(path, check=check)

    if errors:
        print("\n".join(errors))
        return 1

    if check:
        return 0

    if changed:
        print(f"Reformatting: {path}")
        path.write_text(output, "utf-8")

    return 0


def main(check: bool = False) -> int:
    rv = 0
    for _, path in iter_content_paths():
        rv |= _format_file(path, check=check)
    return rv


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        default=False,
        help="Fail if files would be reformatted.",
    )
    args = parser.parse_args()
    sys.exit(main(check=args.check))
