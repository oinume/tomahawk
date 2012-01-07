import os
import sys

def set_lib_path(file):
    parent, bin_dir = os.path.split(os.path.dirname(os.path.abspath(file)))
    for dir in ('lib', ''):
        path = os.path.join(parent, dir)
        if os.path.exists(path):
            sys.path.insert(0, path)
    return parent, bin_dir
