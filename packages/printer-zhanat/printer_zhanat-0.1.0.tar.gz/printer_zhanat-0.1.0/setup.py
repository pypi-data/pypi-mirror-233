# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['printer_zhanat',
 'printer_zhanat.apps',
 'printer_zhanat.apps.client',
 'printer_zhanat.apps.config',
 'printer_zhanat.apps.fastapi_client']

package_data = \
{'': ['*']}

install_requires = \
['escpos>=1.9,<2.0',
 'fastapi>=0.103.1,<0.104.0',
 'pydantic-settings>=2.0.3,<3.0.0',
 'pydantic>=2.3.0,<3.0.0',
 'python-escpos[usb]>=2.2.0,<3.0.0',
 'uvicorn>=0.23.2,<0.24.0']

setup_kwargs = {
    'name': 'printer-zhanat',
    'version': '0.1.0',
    'description': '',
    'long_description': 'Test build packages\n',
    'author': 'Zhanat',
    'author_email': 'janat.200066@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
