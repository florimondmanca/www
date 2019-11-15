from starlette.config import Config

config = Config(".env")

BLOG_ENABLED = config("BLOG_ENABLED", cast=bool, default=False)
