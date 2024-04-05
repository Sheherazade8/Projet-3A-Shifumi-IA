#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages
import sys

NAME = 'shifumy_demo'
DESCRIPTION = 'Python package for Shifumy Demo'
LICENSE = 'GNU General Public License v3 (GPLv3)'
URL = 'https://gitlab.lis-lab.fr/qarma/shifumi2018'.format(NAME)
AUTHOR = 'Mathias Aloui, ' \
         'Valentin Emiya, ' \
         'Luc Giffon, ' \
         'Ama-Marina Kreme, ' \
         'Kilian Macdonald, ' \
         'Liva Ralaivola' \
         'Ibrahim Souleiman-Mahamoud'
AUTHOR_EMAIL = ('valentin.emiya@lis-lab.fr, '
                'ibrahim.souleiman-mahamoud@etu.univ-amu.fr, '
                'luc.giffon@lis-lab.fr, '
                'kilian.macdonald@hotmail.fr, '
                'mathias.aloui@etu.univ-amu.fr, '
                'liva.ralaivola@lis-lab.fr, '
                'ama-marina.kreme@lis-lab.fr, ')
INSTALL_REQUIRES = ['django',
                    'django-globals',
                    'django-extensions',
                    'django-fontawesome',
                    ]
CLASSIFIERS = [
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Natural Language :: English',
    'Operating System :: MacOS :: MacOS X ',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3.5',
]
PYTHON_REQUIRES = '>=3.5'
EXTRAS_REQUIRE = {
    'dev': ['coverage', 'pytest', 'pytest-cov', 'pytest-randomly', 'ipython'],
    'doc': ['sphinx', 'nbsphinx', 'numpydoc', 'sphinx-paramlinks']}
PROJECT_URLS = {'Bug Reports': URL + '/issues',
                'Source': URL}
KEYWORDS = 'shifumi, rock paper scissors, machine learning, artificial ' \
           'intelligence'

###############################################################################
if sys.argv[-1] == 'setup.py':
    print("To install, run 'python setup.py install'\n")

if sys.version_info[:2] < (3, 5):
    errmsg = '{} requires Python 3.5 or later ({[0]:d}.{[1]:d} detected).'
    print(errmsg.format(NAME, sys.version_info[:2]))
    sys.exit(-1)


def get_version():
    v_text = open('VERSION').read().strip()
    v_text_formted = '{"' + v_text.replace('\n', '","').replace(':', '":"')
    v_text_formted += '"}'
    v_dict = eval(v_text_formted)
    return v_dict[NAME]


def set_version(path, VERSION):
    filename = os.path.join(path, '__init__.py')
    buf = ""
    for line in open(filename, "rb"):
        if not line.decode("utf8").startswith("__version__ ="):
            buf += line.decode("utf8")
    f = open(filename, "wb")
    f.write(buf.encode("utf8"))
    f.write(('__version__ = "%s"\n' % VERSION).encode("utf8"))


def setup_package():
    """Setup function"""
    # set version
    VERSION = get_version()

    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

    mod_dir = NAME
    set_version(mod_dir, get_version())
    setup(name=NAME,
          version=VERSION,
          description=DESCRIPTION,
          long_description=long_description,
          url=URL,
          author=AUTHOR,
          author_email=AUTHOR_EMAIL,
          license=LICENSE,
          # classifiers=CLASSIFIERS,
          keywords=KEYWORDS,
          packages=find_packages(exclude=['doc', 'dev']),
          install_requires=INSTALL_REQUIRES,
          python_requires=PYTHON_REQUIRES,
          extras_require=EXTRAS_REQUIRE,
          project_urls=PROJECT_URLS)


if __name__ == "__main__":
    setup_package()
