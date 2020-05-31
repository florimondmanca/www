from setuptools import setup


setup(
    name="sitemaps",
    version="0.0.1",
    py_modules=["sitemaps"],
    install_requires=["httpx", "trio"],
    python_requires=">=3.7",
    license="MIT",
)
