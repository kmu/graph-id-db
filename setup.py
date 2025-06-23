from setuptools import setup

DESCRIPTION = "A database project for graph identification and processing"
NAME = 'graphid-db'
AUTHOR = 'Koki Muraoka, Taku Tanimoto'
AUTHOR_EMAIL = 'muraok_k@chemsys.t.u-tokyo.ac.jp, t_tanimoto@chemsys.t.u-tokyo.ac.jp'
URL = 'https://github.com/chemsys/graphid-db'
LICENSE = 'MIT'
DOWNLOAD_URL = 'https://github.com/chemsys/graphid-db'
VERSION = '0.1.1'
PYTHON_REQUIRES = ">=3.9"
package_data = {'graphid_db' : ['raw/id_jsons/*.json']}

INSTALL_REQUIRES = [
    'pymatgen>=2024.2.20',
    'orjson>=3.10',
]


PACKAGES = [
    'graphid_db',
    'raw',
    'raw.id_jsons',
]

PACKAGE_DATA = {
    'graphid_db': ['raw/id_jsons/*.json']
}


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
      package_data=PACKAGE_DATA,
    )
