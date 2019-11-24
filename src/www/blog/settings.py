import json
import pathlib

HERE = pathlib.Path(__file__).parent
VUEPRESS_DIR = HERE / "site" / ".vuepress"
BUILD_DIR = HERE / "site" / ".vuepress" / "dist"
GENERATED_DIR = HERE / "site" / ".vuepress" / "generated"

assert (
    BUILD_DIR.exists() and GENERATED_DIR.exists()
), "Blog site hasn't been built yet. HINT: $ scripts/build"

with open(GENERATED_DIR / "legacy-blog-url-mapping.json") as f:
    BLOG_LEGACY_URL_MAPPING = json.loads(f.read())

with open(HERE / "site" / ".vuepress" / "config.shared.json") as f:
    config = json.loads(f.read())
    RSS_FEED_PATH = f"/{config['rss_feed_file_name']}"
    del config
