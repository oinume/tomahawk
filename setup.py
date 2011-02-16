from setuptools import setup
import os
from tomahawk.constants import VERSION

def get_long_description():
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README')
    long_description = ''
    try:
        f = open(file)
        long_description = ''.join(f.readlines())
    except IOError:
        print 'Failed to open file "%s".' % (file)
    finally:
        f.close()
    return long_description

setup(
    name = 'tomahawk',
    version = VERSION,
    url = 'http://github.com/oinume/tomahawk/',
    license = 'LGPL',
    author = 'Kazuhiro Oinuma',
    author_email = 'oinume@gmail.com',
    description = 'A simple ssh wrapper for executing commands for many hosts.',
    long_description = get_long_description(),
    packages = [ 'tomahawk' ],
    scripts = [ os.path.join('bin', p) for p in [ 'tomahawk_bootstrap.py', 'tomahawk', 'tomahawk-rsync' ] ],
    zip_safe = False,
    platforms = 'unix',
    install_requires = [
        'argparse',
        'multiprocessing',
        'pexpect>=2.4',
    ],
    test_require = [
        'nose'
    ],
    test_suite = 'nose.collector',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Clustering',
        'Topic :: System :: Systems Administration',
    ],
)
