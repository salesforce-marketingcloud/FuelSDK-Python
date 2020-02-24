class ET_Client_Exception(Exception):
    """
    Base class for all exception happening at the ET_Client level
    """

class ConfigurationException(ET_Client_Exception):
    """
    Raised when an error related to the Client configuration occurs
    """

class AuthException(ET_Client_Exception):
    """
    Raised when the authentication to the Client fails
    """

class WSDLException(ET_Client_Exception):
    """
    Raised when getting the WSDL file fails
    """