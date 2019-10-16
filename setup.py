from os import path
from setuptools import setup
from codecs import open


__package__ = 'gap'
__version__ = '0.10.0'
__licence__ = 'LGPL3'
__author__ = 'Alexandre Decan'
__url__ = 'https://github.com/AlexandreDecan/gap'
__description__ = 'GAP - Git Activity Predictor'


setup(
    name=__package__,
    version=__version__,
    license=__licence__,

    author=__author__,
    url=__url__,

    description=__description__,

    install_requires=[
        'python-dateutil >= 2.7.5',
        'gitpython >= 2.1.11',
        'statsmodels >= 0.9.0',
        'scipy >= 1.1.0',
        'pandas >= 0.23.4',
        'plotnine >= 0.5.1',
    ],

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',

        'Topic :: Scientific/Engineering :: Information Analysis',


        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',

        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='activity prediction git',

    entry_points={
        'console_scripts': [
            'gap=gap:cli',
        ]
    },

    py_modules=['gap'],
    zip_safe=True,
)
