import pathlib

from starlette.config import Config

config = Config(".env")

DIR = pathlib.Path(__file__).parent
DEBUG = config("DEBUG", cast=bool, default=False)
TESTING = config("TESTING", cast=bool, default=False)
