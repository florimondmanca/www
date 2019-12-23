import json
import pathlib

ROOT = pathlib.Path(__file__).parent
CONTENT_ROOT = ROOT / "pages"
ASSETS_ROOT = ROOT / "assets"

with open(ASSETS_ROOT / "legacy-blog-url-mapping.json") as f:
    BLOG_LEGACY_URL_MAPPING = json.loads(f.read())

MARKDOWN_EXTENSIONS = ["codehilite", "fenced_code", "tables"]
