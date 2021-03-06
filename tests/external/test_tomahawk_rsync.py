#from nose.tools import assert_equal, assert_true
import os
from subprocess import call, PIPE
import utils

TOMAHAWK_RSYNC_PATH = os.path.join(utils.get_bin_dir(__file__), 'tomahawk-rsync')
TMP_DIR = os.path.join(utils.get_home_dir(__file__), 'tmp')
if not os.path.exists(TMP_DIR):
    os.mkdir(TMP_DIR)

env = os.environ
if env.get('TOMAHAWK_ENV') != None:
    del env['TOMAHAWK_ENV']

hello_file = os.path.join(TMP_DIR, 'hello')
hello_file_copied = os.path.join(TMP_DIR, 'hello.copied')
if os.path.exists(hello_file_copied):
    os.remove(hello_file_copied)
handle = open(hello_file, 'w')
handle.write('hello world')
handle.close()

def test_03_mirror_mode_pull():
    for f in ('localhost__hello', '127.0.0.1__hello'):
        path = os.path.join(TMP_DIR, f)
        if os.path.exists(path):
            os.remove(path)

    status = call(
        [ TOMAHAWK_RSYNC_PATH, '--hosts=localhost,127.0.0.1', '--mirror-mode=pull',
          hello_file, TMP_DIR ],
        stdout = PIPE, stderr = PIPE
    )

    assert status == 0
    for f in ('localhost__hello', '127.0.0.1__hello'):
        assert os.path.exists(os.path.join(TMP_DIR, f))
