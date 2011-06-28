import os

def get_home_dir(file):
    abspath = os.path.abspath(file)
    parent, dir = None, None
    if abspath.find('internal') != -1 or abspath.find('external') != -1:
        parent, dir = os.path.split(os.path.dirname(os.path.dirname(os.path.abspath(file))))
    else:
        parent, dir = os.path.split(os.path.dirname(os.path.abspath(file)))
    return parent

