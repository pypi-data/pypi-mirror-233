from setuptools import setup, find_packages
import codecs
import os

# If we get stuck, check out this tutorial: https://www.youtube.com/watch?v=tEFkHEKypLI

### To upload to PyPi ###
# pip install wheel
# python setup.py sdist bdist_wheel
# pip install twine
# twine upload dist/*
### Use your PyPi credentials when prompted ###

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

PACKAGE_NAME = "BubbleNova"
VERSION = '0.0.1'
AUTHOR = "SoapDoesCode"
AUTHOR_EMAIL = ""
DESCRIPTION = ""

# Setting up
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['termcolor', 'subprocess', 'threading'], # required packages
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