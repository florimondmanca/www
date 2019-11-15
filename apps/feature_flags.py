from starlette.config import Config

config = Config(".env")

BLOG_ENABLED = config("BLOG_ENABLED", cast=bool, default=False)

variables = dict(locals())

for key, value in variables.items():
    if key.isupper():
        print(f"{key}={value}")
