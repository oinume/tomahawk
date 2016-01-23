import os
import sys
from tomahawk import (
    __author__,
    __author_email__,
    __status__,
    __version__
)

def get_long_description():
    return open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.rst")).read()

try:
    from setuptools import setup
    setup
except ImportError:
    from distutils.core import setup

if sys.version_info < (2, 4):
    print("tomahawk requires at least Python 2.4 to run.")
    sys.exit(1)

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

install_requires = []
if sys.version_info < (2, 6):
    install_requires.extend([ "multiprocessing", "pexpect==2.4", "six==1.2.0" ])
else:
    install_requires.extend([ "six", "pexpect==3.2" ])
if sys.version_info < (2, 7):
    install_requires.append("argparse")

tests_require = [
    'flexmock', 'pytest', 'pytest-cov',
    'sphinx', 'sphinx_rtd_theme',
]

requirements = open("requirements.txt", "w")
requirements.writelines("\n".join(install_requires))
requirements.close()
print("requirements.txt created.")

requirements_dev = open("requirements-dev.txt", "w")
requirements_dev.writelines("\n".join(tests_require))
requirements_dev.close()
print("requirements-dev.txt created")

setup(
    name = "tomahawk",
    version = __version__,
    url = "https://github.com/oinume/tomahawk/",
    license = "LGPL",
    author = __author__,
    author_email = __author_email__,
    description = "A simple ssh wrapper to execute commands for many hosts.",
    long_description = get_long_description(),
    packages = [ "tomahawk" ],
    scripts = [ os.path.join("bin", p) for p in [ "tomahawk", "tomahawk-rsync" ] ],
    zip_safe = False,
    platforms = "unix",
    install_requires = install_requires,
    tests_require = tests_require,
    data_files = [
        ("man/man1", [ "man/man1/tomahawk.1", "man/man1/tomahawk-rsync.1" ])
    ],
    classifiers = [
        "Development Status :: 5 - " + __status__,
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Clustering",
        "Topic :: System :: Systems Administration",
    ],
)
