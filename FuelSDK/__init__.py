__version__ = '1.3.0'

# Runtime patch the suds library
from FuelSDK.suds_patch import _PropertyAppender
from suds.mx import appender as _appender
_appender.PropertyAppender = _PropertyAppender

from FuelSDK.suds_patch import _bodycontent
from suds.bindings import document as _document
_document.Document.bodycontent = _bodycontent
# end runtime patching of suds

from FuelSDK.client import ET_Client

# Import all the wrapper objects
from FuelSDK.objects import *
