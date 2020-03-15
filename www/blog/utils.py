import glob
from pathlib import Path
from typing import Iterator


def find_markdown_files(root: Path) -> Iterator[Path]:
    pattern = str(root / "**" / "*.md")
    for path in glob.glob(pattern, recursive=True):
        yield Path(path)
