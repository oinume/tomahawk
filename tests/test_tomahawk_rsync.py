from nose.tools import assert_equal, assert_true
import os
import tempfile
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

def test_01_basic():

    status = call(
        [ TOMAHAWK_RSYNC_PATH, '--hosts=localhost', hello_file, hello_file_copied ],
        stdout = PIPE, stderr = PIPE
    )
    assert_equal(status, 0, "rsync (basic)")
    assert_true(os.path.exists(hello_file_copied), "rsync (basic)")

def test_02_rsync_options():
#    status = call(
#        [ TOMAHAWK_RSYNC_PATH, '--hosts=localhost', '--dry-run',
#          os.path.join(TMP_DIR, ''), tempfile.gettempdir() ],
#        stdout = PIPE, stderr = PIPE
#    )
#    assert_equal(status, 0, "rsync (--rsync-options)")

    status = call(
        [ TOMAHAWK_RSYNC_PATH, '--hosts=localhost', '-o=-av --dry-run',
          os.path.join(TMP_DIR, ''), tempfile.gettempdir() ],
        stdout = PIPE, stderr = PIPE
    )
    assert_equal(status, 0, "rsync (--rsync-options)")

def test_03_mirror_mode_pull():
    for f in ('localhost__hello', '127.0.0.1__hello'):
        path = os.path.join(TMP_DIR, f)
        if os.path.exists(path):
            os.remove(path)

    status = call(
        [ TOMAHAWK_RSYNC_PATH, '--hosts=localhost,127.0.0.1', '--mirror-mode=pull',
          hello_file, TMP_DIR ],
        stdout = PIPE, stderr = PIPE)

    assert_equal(status, 0, "rsync (--mirror-mode=pull)")
    for f in ('localhost__hello', '127.0.0.1__hello'):
        print os.path.exists(os.path.join(TMP_DIR, f))
        assert_true(
            os.path.exists(os.path.join(TMP_DIR, f)),
            "rsync (--mirror-mode=pull:%s exists)" % (f)
        )
