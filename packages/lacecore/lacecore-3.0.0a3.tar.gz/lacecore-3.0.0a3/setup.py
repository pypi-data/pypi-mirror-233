# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lacecore',
 'lacecore._analysis',
 'lacecore._cli',
 'lacecore._common',
 'lacecore._obj',
 'lacecore._selection',
 'lacecore._transform',
 'lacecore.shapes']

package_data = \
{'': ['*']}

install_requires = \
['numpy', 'ounce>=1.1.0,<2.0', 'polliwog>=3.0.0a3', 'vg>=2.0.0']

extras_require = \
{'cli': ['click>=8.1.3,<9', 'tinymetabobjloader==2.0.0a0'],
 'obj': ['tinymetabobjloader==2.0.0a0']}

entry_points = \
{'console_scripts': ['convert_units = '
                     'lacecore_cli.convert_units:convert_units']}

setup_kwargs = {
    'name': 'lacecore',
    'version': '3.0.0a3',
    'description': 'Polygonal meshes optimized for cloud computation',
    'long_description': 'None',
    'author': 'Paul Melnikow',
    'author_email': 'github@paulmelnikow.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lace/lacecore',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
