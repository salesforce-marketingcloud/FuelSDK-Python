import copy
from unittest import TestCase
from FuelSDK import ET_Client
from FuelSDK.exceptions import ConfigurationException


class TestET_Client_Errors(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_params = {
            'clientid': 'clientid',
            'clientsecret': 'clientsecret',
            'defaultwsdl': 'https://webservice.exacttarget.com/etframework.wsdl',
            'authenticationurl': '',
            'baseapiurl': 'https://webservice.exacttarget.com/',
            'soapendpoint': 'https://webservice.exacttarget.com/',
            'wsdl_file_local_loc': '/tmp/ExactTargetWSDL.s6.xml',
            'useOAuth2Authentication': 'False',
            'accountId': 'accountId',
            'scope': 'scope',
            'applicationType': 'server',
            'redirectURI': 'https://webservice.exacttarget.com/redirect',
            'authorizationCode': 'authorizationCode',
        }
    
    def test_should_throw_configexception_if_wrong_application_type(self):
        params = copy.deepcopy(self.base_params)
        params['applicationType'] = 'dummy'

        with self.assertRaises(ConfigurationException):
            ET_Client(False, False, params=params)

    def test_should_throw_configexception_if_no_authurl_and_oauth2_enabled(self):
        params = copy.deepcopy(self.base_params)
        params['useOAuth2Authentication'] = 'True'
        params['authenticationurl'] = ''

        with self.assertRaises(ConfigurationException):
            ET_Client(False, False, params=params)

    def test_should_throw_configexception_if_public_app_and_no_redirecturi(self):
        params = copy.deepcopy(self.base_params)
        params['applicationType'] = 'public'
        params['redirectURI'] = ''

        with self.assertRaises(ConfigurationException):
            ET_Client(False, False, params=params)

    def test_should_throw_configexception_if_web_app_and_no_redirecturi(self):
        params = copy.deepcopy(self.base_params)
        params['applicationType'] = 'web'
        params['redirectURI'] = ''

        with self.assertRaises(ConfigurationException):
            ET_Client(False, False, params=params)
    
    def test_should_throw_configexception_if_public_app_and_no_authcode(self):
        params = copy.deepcopy(self.base_params)
        params['applicationType'] = 'public'
        params['authorizationCode'] = ''

        with self.assertRaises(ConfigurationException):
            ET_Client(False, False, params=params)

    def test_should_throw_configexception_if_web_app_and_no_authcode(self):
        params = copy.deepcopy(self.base_params)
        params['applicationType'] = 'web'
        params['authorizationCode'] = ''

        with self.assertRaises(ConfigurationException):
            ET_Client(False, False, params=params)

    def test_should_throw_configexception_if_public_app_and_no_clientid(self):
        params = copy.deepcopy(self.base_params)
        params['applicationType'] = 'public'
        params['clientid'] = ''

        with self.assertRaises(ConfigurationException):
            ET_Client(False, False, params=params)

    def test_should_throw_configexception_if_web_app_and_no_clientid(self):
        params = copy.deepcopy(self.base_params)
        params['applicationType'] = 'web'
        params['clientid'] = ''

        with self.assertRaises(ConfigurationException):
            ET_Client(False, False, params=params)
    
    def test_should_throw_configexception_if_web_app_and_no_clientsecret(self):
        params = copy.deepcopy(self.base_params)
        params['applicationType'] = 'web'
        params['clientsecret'] = ''

        with self.assertRaises(ConfigurationException):
            ET_Client(False, False, params=params)

    def test_should_throw_configexception_if_server_app_and_no_clientid(self):
        params = copy.deepcopy(self.base_params)
        params['applicationType'] = 'server'
        params['clientid'] = ''

        with self.assertRaises(ConfigurationException):
            ET_Client(False, False, params=params)
    
    def test_should_throw_configexception_if_server_app_and_no_clientsecret(self):
        params = copy.deepcopy(self.base_params)
        params['applicationType'] = 'server'
        params['clientsecret'] = ''

        with self.assertRaises(ConfigurationException):
            ET_Client(False, False, params=params)