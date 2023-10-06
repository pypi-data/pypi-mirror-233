from pathlib import Path
from setuptools import find_packages, setup

# Package meta-data.
NAME = 'anywebscraper'
DESCRIPTION = "anywebscraper is your ultimate web data extraction companion. We understand the challenges of web scraping, including dealing with anti-bot measures and the need for reliable proxies. We make web scraping easy and effective, even in the most challenging environments. Whether you're a data scientist, business analyst or developer looking to harness the power of web data, anywebscraper has you covered."

URL = "https://github.com/pierjosvins/anywebscraper"
EMAIL = "colerepierjos30@gmail.com"
AUTHOR = "Pierjos COLERE"
REQUIRES_PYTHON = ">=3.6.0"


# Load the package's VERSION
ROOT_DIR = Path(__file__).resolve().parent
REQUIREMENTS_DIR = ROOT_DIR / 'requirements'
VERSION = "0.1.3"
PACKAGE_DIR = ROOT_DIR / 'anywebscraper'
with open(str(ROOT_DIR / 'Readme.md'), 'r') as fd:
    long_description = fd.read()

# What packages are required for this module to be executed?
def list_reqs(fname="requirements.txt"):
    with open(str(REQUIREMENTS_DIR / fname), 'r') as fd:
        return fd.read().splitlines()

# all these information are passed to setup:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=("tests",)),
    install_requires=list_reqs(),
    extras_require={},
    license="",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: PyPy",
	"Operating System :: Unix",
	"Operating System :: MacOS :: MacOS X",
	"Operating System :: Microsoft :: Windows",
    ],
)
