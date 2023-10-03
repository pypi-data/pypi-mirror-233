# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['peakventures']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.28.11,<2.0.0',
 'requests>=2.31.0,<3.0.0',
 'tenacity>=8.2.2,<9.0.0',
 'websockets>=11.0.3,<12.0.0']

setup_kwargs = {
    'name': 'peakventures',
    'version': '1.2.8',
    'description': 'PeakVentures Python Utilities',
    'long_description': 'None',
    'author': 'Volodymyr Smirnov',
    'author_email': 'volodymyr@peakventures.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
