import pathlib

from starlette.config import Config

from apps import feature_flags

config = Config()

DIR = pathlib.Path(__file__).parent
DEBUG = config("DEBUG", cast=bool, default=False)
TESTING = config("TESTING", cast=bool, default=False)
BLOG_URL = "/blog/" if feature_flags.BLOG_ENABLED else "https://blog.florimond.dev"
