# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonnotate']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jsonnotate',
    'version': '0.2.2',
    'description': '',
    'long_description': None,
    'author': 'Edward George',
    'author_email': 'edwardgeorge@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
