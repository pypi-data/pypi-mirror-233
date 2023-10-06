from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Faster pattern matching in text processing and data analysis.'
LONG_DESCRIPTION = 'Pattern Pursuit Library: Efficient Pattern Matching Algorithms including KMP, Boyer-Moore, and Rabin-Karp with Dynamic Selection'

# Setting up
setup(
    name="patternSense",
    version=VERSION,
    author="Sagar Nailwal",
    author_email="<sanjunailwal2003@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['timeit'],
    keywords=['patter_matching','Rabin Karp','Boyer Moore','KMP'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)