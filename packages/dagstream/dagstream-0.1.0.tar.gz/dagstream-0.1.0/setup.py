# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dagstream',
 'dagstream.graph_components',
 'dagstream.graph_components.dags',
 'dagstream.graph_components.nodes',
 'dagstream.utils',
 'dagstream.viewers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dagstream',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'sakamoto',
    'author_email': 'sakamoto@ricos.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
