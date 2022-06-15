import os

''' defines the path name of the directory containing the directory that contains this module '''
''' i.e. defines the path name of the direcctory containing config/ regardless of user's machine '''
ROOT_DIR = ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
