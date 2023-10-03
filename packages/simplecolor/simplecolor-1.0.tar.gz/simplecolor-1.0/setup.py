from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0'
DESCRIPTION = 'SimpleColor - Add colors to your terminal output easily'
LONG_DESCRIPTION = 'SimpleColor is a Python module that allows you to add colors to your terminal output with ease.'

setup(
    name="simplecolor",
    version=VERSION,
    author="VisuallySynced",
    author_email="",  
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],  
    keywords=['python', 'color', 'terminal output', 'text color', 'terminal formatting'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
