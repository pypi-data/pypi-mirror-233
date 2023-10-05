# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['macrometa_target_s3', 'macrometa_target_s3.formats']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.28.40,<1.29.0',
 'c8connector>=0.0.32',
 'numpy>=1.23.4,<2.0.0',
 'pandas>=1.5.1,<2.0.0',
 'prometheus-client==0.16.0',
 'pyarrow>=10.0.0,<11.0.0',
 'pymongo>=4.3.3,<5.0.0',
 'requests>=2.25.1,<3.0.0',
 'singer-sdk>=0.30.0,<0.31.0',
 'smart-open[s3]>=6.3.0,<7.0.0']

entry_points = \
{'console_scripts': ['macrometa-target-s3 = '
                     'macrometa_target_s3.target:Targets3.cli']}

setup_kwargs = {
    'name': 'macrometa-target-s3',
    'version': '0.0.14',
    'description': '`macrometa-target-s3` is a Singer target for s3, built with the Meltano Singer SDK.',
    'long_description': 'None',
    'author': 'crowemi',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<3.11',
}


setup(**setup_kwargs)
