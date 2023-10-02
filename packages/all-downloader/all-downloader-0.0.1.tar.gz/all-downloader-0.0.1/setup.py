# -*- coding: utf-8 -*-
import os
import sys
from distutils.core import setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 5)

sys.path.append('all-downloader')


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        "This version of Python Youtube API requires Python {}.{}, but you're trying to install it on Python {}.{}."
        .format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)
setup(
    name='all-downloader',
    version='0.0.1',
    description='The full package for download from several platforms',
    author=u'Jahongir Ibragimov',
    author_email='chogirmali.yigit@gmail.com',
    url='https://github.com/xalq-mazza-qilsin/downloader-API',
    packages=['all-downloader'],
    keywords="python video audio download",
    long_description=read('README.rst'),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: XML'
    ],
    license='MIT'
)
