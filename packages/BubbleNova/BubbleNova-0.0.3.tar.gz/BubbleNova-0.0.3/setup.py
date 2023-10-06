from setuptools import setup, find_packages
import codecs
import os

# If we get stuck, check out this tutorial: https://www.youtube.com/watch?v=tEFkHEKypLI

### To upload to PyPi ###
# pip install setuptools --upgrade
# pip install wheel --upgrade
# pip install twine --upgrade
# python setup.py sdist bdist_wheel
# twine upload dist/*
### Use your PyPi credentials when prompted ###

here = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r") as fh:
    long_description = fh.read()

PACKAGE_NAME = "BubbleNova"
VERSION = '0.0.3'
AUTHOR = "SoapDoesCode"
AUTHOR_EMAIL = ""
DESCRIPTION = "A Python library for running multiple Discord bots at once."

# Setting up
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[], # required packages
    keywords=['python', 'discord', 'disord bot', 'bubble nova'],
    classifiers=[
        "Development Status :: 1 - Planning", # https://pypi.org/classifiers/
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)