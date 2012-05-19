from setuptools import setup
import os
import sys
from tomahawk import (
    __author__,
    __author_email__,
    __status__,
    __version__
)

def get_long_description():
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.rst')
    long_description = ''
    try:
        f = open(file)
        long_description = ''.join(f.readlines())
        f.close()
    except IOError:
        print 'Failed to open file "%s".' % (file)
        f.close()
    return long_description


install_requires = [ 'pexpect >= 2.4' ]
if sys.version_info < (2, 7):
    install_requires.append('argparse')
if sys.version_info < (2, 6):
    install_requires.append('multiprocessing')

setup(
    name = 'tomahawk',
    version = __version__,
    url = 'http://github.com/oinume/tomahawk/',
    license = 'LGPL',
    author = __author__,
    author_email = __author_email__,
    description = 'A simple ssh wrapper for executing commands for many hosts.',
    long_description = get_long_description(),
    packages = [ 'tomahawk' ],
    scripts = [ os.path.join('bin', p) for p in [ 'tomahawk', 'tomahawk-rsync' ] ],
    zip_safe = False,
    platforms = 'unix',
    install_requires = install_requires,
    tests_require = [
#        'nose >= 0.11',
        'mock',
        'pytest',
    ],
    test_suite = 'nose.collector',
    classifiers = [
        'Development Status :: 5 - ' + __status__,
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Clustering',
        'Topic :: System :: Systems Administration',
    ],
)
