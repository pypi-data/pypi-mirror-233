# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cybsi',
 'cybsi.cloud',
 'cybsi.cloud.auth',
 'cybsi.cloud.internal',
 'cybsi.cloud.iocean']

package_data = \
{'': ['*']}

install_requires = \
['enum-tools==0.9.0.post1', 'httpx>=0.23.1,<0.24.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=4.1.1,<5.0.0']}

setup_kwargs = {
    'name': 'cybsi-cloud-sdk',
    'version': '1.0.4',
    'description': 'Cybsi Cloud development kit',
    'long_description': 'Cybsi Cloud SDK\n---------------\nPython SDK для лёгкой интеграции с сервисами Cybsi Cloud (https://cybsi.cloud). Cybsi Cloud предоставляет данные о киберугрозах.\n\nБиблиотека имеет как синхронный, так и асинхронный интерфейс.\n\n[![Supported Versions](https://img.shields.io/pypi/pyversions/cybsi-cloud-sdk.svg)](https://pypi.org/project/cybsi-cloud-sdk/)\n[![Documentation Status](https://readthedocs.org/projects/cybsi-cloud-sdk/badge/?version=latest)](https://cybsi-cloud-sdk.readthedocs.io/en/latest/?badge=latest)',
    'author': 'Cybsi Cloud developers',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
