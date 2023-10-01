#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['sec_edgar_downloader']

package_data = \
{'': ['*']}

install_requires = \
['requests', 'pyrate-limiter>=3.1.0']

extras_require = \
{'doc': ['doc8', 'sphinx', 'sphinx-autobuild', 'sphinx-autodoc-typehints'],
 'test': ['pre-commit', 'pytest', 'pytest-cov']}

setup(name='sec-edgar-downloader',
      version='5.0.1',
      description='Download SEC filings from the EDGAR database using Python',
      author=None,
      author_email='Jad Chaar <jad.chaar@gmail.com>',
      url=None,
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      extras_require=extras_require,
      python_requires='>=3.8',
     )
