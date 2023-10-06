# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bert_schemas',
 'bert_schemas.testing',
 'bert_schemas.testing.factories',
 'bert_schemas.testing.fixtures']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.2,<3.7.0',
 'polyfactory>=2.8.0,<3.0.0',
 'pydantic[email]>=2.3.0,<3.0.0',
 'pytest>=7.4.2,<8.0.0',
 'scipy>=1.10.0,<2.0.0']

setup_kwargs = {
    'name': 'bert-schemas',
    'version': '2.0.5',
    'description': 'Bert service schemas',
    'long_description': '# Bert Schemas\n\n[![License: Apache](https://img.shields.io/badge/License-Apache-yellow.svg)](https://opensource.org/licenses/Apache-2.0) [![Twitter](https://img.shields.io/twitter/url/https/twitter.com/Infleqtion.svg?style=social&label=Follow%20%40Infleqtion)](https://twitter.com/Infleqtion)\n\n## 🚀 Quick Install\n\n```python\npip install bert-schemas\n```\n\n## 🧭 Introduction\n\nThese Pydantic schemas are used by projects such as Oqtant for defining and validating REST payloads.\n',
    'author': 'Larry Buza',
    'author_email': 'lawrence.buza@coldquanta.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<3.12',
}


setup(**setup_kwargs)
