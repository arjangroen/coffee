from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
#import codecs
import os
import sys

import sandman

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.txt', 'CHANGES.txt')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='coffee',
    version=sandman.__version__,
    url='http://github.com/arjangroen/coffee/',
    license='Apache Software License',
    author='Arjan Groen',
    tests_require=['pytest'],
    install_requires=['matplotlib>=0.10.1',
                    'pandas>=0.20.1',
                    'dominate>=2.3.1',
                    'numpy>=1.12.1'
                    ],
    cmdclass={'test': PyTest},
    author_email='arjanmartengroen@gmail.com',
    description='Grab a coffee and quickly scan through your data',
    long_description=long_description,
    packages=['coffee'],
    include_package_data=True,
    platforms='any',
    test_suite='coffee.test.test_coffee',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 1 - Beta',
        'Natural Language :: English',
        'Environment :: Python',
        'Intended Audience :: Data Scientist / Data analysts',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    extras_require={
        'testing': ['pytest'],
    }
)