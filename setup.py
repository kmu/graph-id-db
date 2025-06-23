from setuptools import setup
from graphid_db.finder import Finder

DESCRIPTION = "A database project for graph identification and processing"
NAME = 'graphid-db'
AUTHOR = 'Koki Muraoka, Taku Tanimoto'
AUTHOR_EMAIL = 'muraok_k@chemsys.t.u-tokyo.ac.jp, t_tanimoto@chemsys.t.u-tokyo.ac.jp'
URL = 'https://github.com/chemsys/graphid-db'
LICENSE = 'MIT'
DOWNLOAD_URL = 'https://github.com/chemsys/graphid-db'
VERSION = '0.1.0'
PYTHON_REQUIRES = ">=3.9"

INSTALL_REQUIRES = [
    'pymatgen>=2024.2.20',
    'orjson>=3.10',
]


PACKAGES = [
    'filebase',
    'graphid_db'
]


setup(name=NAME,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      license=LICENSE,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      python_requires=PYTHON_REQUIRES,
      install_requires=INSTALL_REQUIRES,
      packages=PACKAGES,
    )
