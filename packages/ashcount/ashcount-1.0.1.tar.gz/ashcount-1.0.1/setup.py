import os
from setuptools import setup

with open("README.md", "r") as file:
    long_desc = file.read()

setup(
    name = "ashcount",
    version = "1.0.1",
    author = "Ashkan Noroozi",
    author_email = "ashkan02011@gmail.com",
    description = ("A set of things that can be done with files. For example, finding the number of lines in a file Find the number of words Find the net code count of a Python file."),
    license = "MIT",
    keywords = ['python', 'package'],
    url = "https://github.com/ashkan0201/ashcount",
    packages=['ashcount'],
    long_description = long_desc,
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)