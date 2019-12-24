import pathlib

from starlette.config import Config

config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
TESTING = config("TESTING", cast=bool, default=False)

WEB_ROOT = pathlib.Path(__file__).parent
WEB_DD_TRACE_SERVICE = config("DD_TRACE_SERVICE", cast=str, default="")
WEB_DD_TRACE_TAGS = config("DD_TRACE_TAGS", cast=str, default="")
