from os import path
from setuptools import setup, find_packages

this_directory = path.dirname(__file__)
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="solari",
    packages=find_packages(),
    python_requires='>=3.8',
    version="0.1.0",
    install_requires=["pandas"],
    description="Library for high level statistical analysis on bulk match data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Canisback",
    author_email="canisback@gmail.com",
    url="https://github.com/Canisback/solari",
    keywords=["Riot Games API","Riot API","stats","League of Legends"],
    classifiers=[]
)
