from six import print_
import os
import utils
utils.append_home_to_path(__file__)

from tomahawk.utils import (
    get_options_from_conf
)

def test_00_get_options_from_conf(tmpdir):
    path = os.path.join(str(tmpdir), 'tomahawk.conf')
    conf = open(path, 'w')
    try:
        conf.write("""
[tomahawk]
options = --verify-output
""".strip())
    finally:
        conf.close()
    conf_options = get_options_from_conf('tomahawk', path)
    assert conf_options == [ '--verify-output' ]

def test_01_get_options_from_conf_no_options(tmpdir):
    path = os.path.join(str(tmpdir), 'tomahawk.conf')
    conf = open(path, 'w')
    try:
        conf.write("""
[tomahawk]
# options = --verify-output
""".strip())
    finally:
        conf.close()
    conf_options = get_options_from_conf('tomahawk', path)
    assert conf_options == []

