class ConfigurationException(Exception):
    """
    Raised when an error related to the Client configuration occurs
    """

class AuthException(Exception):
    """
    Raised when the authentication to the Client fails
    """

class WSDLException(Exception):
    """
    Raised when getting the WSDL file fails
    """