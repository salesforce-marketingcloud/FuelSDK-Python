import version

__version__ = version.get()

# Runtime patch the suds library
from FuelSDK.suds_patch import _PropertyAppender
from suds.mx import appender as _appender
_appender.PropertyAppender = _PropertyAppender

from FuelSDK.suds_patch import _bodycontent
from suds.bindings import document as _document
_document.Document.bodycontent = _bodycontent
from FuelSDK.suds_patch import _start
from suds.mx import literal as _literal
_literal.Typed.start = _start
# end runtime patching of suds

from FuelSDK.client import ET_Client

# Import all the wrapper objects
from FuelSDK.objects import *
