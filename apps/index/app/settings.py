import pathlib

from starlette.config import Config


config = Config()

DIR = pathlib.Path(__file__).parent.parent
DEBUG = config("DEBUG", cast=bool, default=False)
TESTING = config("TESTING", cast=bool, default=False)
