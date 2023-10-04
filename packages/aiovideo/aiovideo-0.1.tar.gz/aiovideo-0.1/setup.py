import setuptools
from pathlib import Path

setuptools.setup(
    name="aiovideo",
    description="This library used for download videos from Youtube platform!",
    long_description=Path("README.md").read_text(),
    version="0.1",
    packages=setuptools.find_packages(exclude=["tests", "data"])
)