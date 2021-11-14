from typing import List, Text
import nasa

from setuptools import setup

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements: List[Text] = ["requests"]

setup(
    name="nasa",
    version=nasa.__version__,
    description="Unofficial Python Wrapper for NASA API",
    author="Faisal Malik",
    author_email="faisalmalikwidyaprasetya@gmail.com",
    packages=["nasa"],
    package_dir={"nasa": "nasa"},
    include_package_data=True,
    license="MIT",
    requires=requirements,
)
