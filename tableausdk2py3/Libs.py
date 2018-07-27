# -----------------------------------------------------------------------------
#
# This file is the copyrighted property of Tableau Software and is protected
# by registered patents and other applicable U.S. and international laws and
# regulations.
#
# Unlicensed use of the contents of this file is prohibited. Please refer to
# the NOTICES.txt file for further details.
#
# -----------------------------------------------------------------------------

import ctypes
import os
import sys
os.environ['PATH'] = os.path.join(os.path.dirname(__file__), 'bin') + os.pathsep + os.environ['PATH']

LIBS = ['Common', 'Extract', 'HyperExtract', 'Server']

if sys.platform == 'win32':
    LIB_PATHS = dict((lib_name, 'Tableau' + lib_name) for lib_name in LIBS)
elif sys.platform.startswith('linux'):
    LIB_PATHS = dict((lib_name, os.path.join(os.path.dirname(__file__), 'lib', 'libTableau' + lib_name + '.so')) for lib_name in LIBS)
elif sys.platform == 'darwin':
    LIB_PATHS = dict((lib_name, os.path.join(os.path.dirname(__file__), 'lib', 'libTableau' + lib_name + '.dylib')) for lib_name in LIBS)
else:
   raise RuntimeError('Unknown platform ' + sys.platform)

class LoadLibs(object):
    def __init__(self, lib_path = LIB_PATHS):
        self.lib_paths = LIB_PATHS
        self.libs = {}
        self.is_lib_loaded = dict((lib_name, False) for lib_name in LIBS)

    def load_lib(self, lib_name):
        if not self.is_lib_loaded[lib_name]:
            self.libs[lib_name] = ctypes.cdll.LoadLibrary(self.lib_paths[lib_name])
            self.is_lib_loaded[lib_name] = True
        return self.libs[lib_name]
