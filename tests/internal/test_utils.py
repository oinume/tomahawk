import os
import utils
utils.append_home_to_path(__file__)

from tomahawk.utils import (
    get_options_from_conf
)

def test_00_get_options_from_conf(tmpdir):
    os.environ['HOME'] = str(tmpdir)
    path = os.path.join(str(tmpdir), '.tomahawk.conf')
    conf = open(path, 'w')
    try:
        conf.write("""
[tomahawk]
options = --verify-output
""".strip())
    finally:
        conf.close()
    conf_options, conf_path = get_options_from_conf('tomahawk')
    print conf_options
    assert conf_options == [ '--verify-output' ]
    assert conf_path == path
