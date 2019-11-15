from setuptools import setup, find_packages

setup(
    name="www",
    python_requires=">=3.7",
    install_requires=[
        "aiofiles==0.4.*",
        "ddtrace==0.30.*",
        "ddtrace-asgi==0.3.*",
        "gunicorn==19.*",
        "jinja2==2.*",
        "starlette==0.13.*",
        "uvicorn==0.10.*",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    classifiers=["Private :: Do Not Upload"],
)
