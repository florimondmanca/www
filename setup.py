from setuptools import setup

setup(
    name="www",
    python_requires=">=3.7",
    install_requires=[
        "aiofiles==0.4.*",
        "gunicorn==19.*",
        "jinja2==2.*",
        "starlette==0.13.*",
        "uvicorn==0.10.*",
        "tldextract==2.2.*",
    ],
    classifiers=["Private :: Do Not Upload"],
)
