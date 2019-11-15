import pathlib

from starlette.config import Config

config = Config(".env")

DIR = pathlib.Path(__file__).parent
DD_TRACE_SERVICE = config("DD_TRACE_SERVICE", cast=str, default="")
DD_TRACE_TAGS = config("DD_TRACE_TAGS", cast=str, default="")
DEBUG = config("DEBUG", cast=bool, default=False)
TESTING = config("TESTING", cast=bool, default=False)
