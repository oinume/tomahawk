import os
import sys

def get_home_dir(file):
    abspath = os.path.abspath(file)
    parent, dir = None, None
    for dir in ( 'internal', 'internal2', 'external' ):
        if abspath.find(dir) != -1:
            return os.path.split(os.path.dirname(os.path.dirname(os.path.abspath(file))))[0]
    return os.path.split(os.path.dirname(os.path.abspath(file)))[0]

def get_bin_dir(file):
    return os.path.join(get_home_dir(file), 'bin')

def append_home_to_path(file):
    sys.path.insert(0, get_home_dir(file))
