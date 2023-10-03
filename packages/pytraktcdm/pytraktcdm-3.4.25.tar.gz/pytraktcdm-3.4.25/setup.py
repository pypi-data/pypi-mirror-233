from setuptools import setup

import trakt

__author__ = 'Chris Martinez, Elan Ruusamäe, Jon Nappi'

with open('README.rst') as f:
    readme = f.read()
with open('HISTORY.rst') as f:
    history = f.read()
with open('requirements.txt') as f:
    requires = [line.strip() for line in f if line.strip()]

packages = ['trakt']
description = ('Pythonic abstraction layer for easier scripting of the '
               'Trakt.tv REST API.')

setup(
    name='pytraktcdm',
    version=trakt.__version__,
    description=description,
    long_description='\n'.join([readme, history]),
    author='Chris Martinez',
    author_email='chris@chrismartinez.net',
    url='https://github.com/chrisdma/python-pytrakt',
    packages=packages,
    install_requires=requires,
    license='Apache 2.0',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Freely Distributable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9']
)
