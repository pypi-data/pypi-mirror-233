# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['data_transformation_tc']
install_requires = \
['numpy>=1.24.2,<2.0.0']

setup_kwargs = {
    'name': 'data-transformation-tc',
    'version': '0.1.1',
    'description': 'data_transformation_tc is a Python library designed to streamline common data transformations required in machine learning and data science workflows, such as transpose a matrix, create time series windows, or apply 2D convolution',
    'long_description': None,
    'author': '______________',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
