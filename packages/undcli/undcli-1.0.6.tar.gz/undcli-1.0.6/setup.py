# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['undcli', 'undcli.commands']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.28.60,<2.0.0',
 'google-cloud-storage>=2.11.0,<3.0.0',
 'tqdm>=4.66.1,<5.0.0',
 'typer[all]>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['mlp = undcli.main:app']}

setup_kwargs = {
    'name': 'undcli',
    'version': '1.0.6',
    'description': '',
    'long_description': None,
    'author': 'Aayushman Choudhary',
    'author_email': 'aayushmanchaudhory@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
