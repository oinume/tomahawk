from nose.tools import assert_equal, assert_true
import os
import tempfile
from subprocess import call, PIPE
import utils

TOMAHAWK_RSYNC_PATH = os.path.join(utils.get_bin_dir(__file__), 'tomahawk-rsync')
TMP_DIR = os.path.join(utils.get_home_dir(__file__), 'tmp')
if not os.path.exists(TMP_DIR):
    os.mkdir(TMP_DIR)

def test_01_basic():
    hello_file = os.path.join(TMP_DIR, 'hello')
    hello_file_copied = os.path.join(TMP_DIR, 'hello.copied')
    if os.path.exists(hello_file_copied):
        os.remove(hello_file_copied)
    handle = open(hello_file, 'w')
    handle.write('hello world')
    handle.close()
    
    status = call(
        [ TOMAHAWK_RSYNC_PATH, '--hosts=localhost', hello_file, hello_file_copied ],
        stdout = PIPE, stderr = PIPE
    )
    assert_equal(status, 0, 'rsync (basic)')
    assert_true(os.path.exists(hello_file_copied), 'rsync (basic)')

def test_02_rsync_options():
    status = call(
        [ TOMAHAWK_RSYNC_PATH, '--hosts=localhost', '-o=-av --dry-run',
          os.path.join(TMP_DIR, ''), tempfile.gettempdir() ],
        stdout = PIPE, stderr = PIPE
    )
    assert_equal(status, 0, 'rsync (--rsync_options)')
