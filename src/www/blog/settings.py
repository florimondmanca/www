import json
import pathlib

HERE = pathlib.Path(__file__).parent
BUILD_DIR = HERE / "site" / ".vuepress" / "dist"
GENERATED_DIR = HERE / "site" / ".vuepress" / "generated"

assert (
    BUILD_DIR.exists() and GENERATED_DIR.exists()
), "Blog site hasn't been built yet. HINT: $ scripts/build"

with open(GENERATED_DIR / "legacy-blog-url-mapping.json") as f:
    BLOG_LEGACY_URL_MAPPING = json.loads(f.read())
