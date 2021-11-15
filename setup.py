from typing import List, Text
import nasa

from setuptools import setup

with open("README.md") as readme_file:
    readme: Text = readme_file.read()

requirements: List[Text] = ["requests"]

setup(
    name="python-nasa",
    version=nasa.__version__,
    description="Unofficial Python Wrapper for NASA API",
    long_description=readme,
    long_description_content_type="text/markdown",
    author=nasa.__author__,
    author_email=nasa.__email__,
    packages=["nasa"],
    package_dir={"nasa": "nasa"},
    include_package_data=True,
    license="MIT",
    requires=requirements,
    keywords="nasa planet astronomy image galaxy earth",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
