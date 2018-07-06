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

from ctypes import *
from . import Libs

class TableauException(Exception):
    def __init__(self, errorCode, message):
        Exception.__init__(self, message)
        self.errorCode = errorCode
        self.message = message

    def __str__(self):
        return 'TableauException ({0}): {1}'.format(self.errorCode, self.message)

def GetLastErrorMessage():
    common_lib = Libs.LoadLibs().load_lib('Common')
    common_lib.TabGetLastErrorMessage.argtypes = []
    common_lib.TabGetLastErrorMessage.restype = c_wchar_p

    return wstring_at(common_lib.TabGetLastErrorMessage())