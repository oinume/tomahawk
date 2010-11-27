import os

def get_home_dir(file):
    parent, dir = os.path.split(os.path.dirname(os.path.abspath(file)))
    return parent

def get_bin_dir(file):
    return os.path.join(get_home_dir(file), 'bin')
