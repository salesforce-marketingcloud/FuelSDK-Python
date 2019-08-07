import os
import logging
import configparser
import time
import json

import jwt
import requests
import suds.client
import suds.wsse
from suds.sax.element import Element


from FuelSDK.objects import ET_DataExtension,ET_Subscriber


class ET_Client(object):
    """
    Setup web service connectivity by getting need config data, security tokens etc.
    """

    debug = False
    client_id = None
    client_secret = None
    appsignature = None
    wsdl_file_url = None
    authToken = None
    internalAuthToken = None
    authTokenExpiration = None  #seconds since epoch that the current jwt token will expire
    refreshKey = None
    endpoint = None
    authObj = None
    soap_client = None
    auth_url = None
    soap_endpoint = None
    soap_cache_file = "soap_cache_file.json"
    use_oAuth2_authentication = None
    account_id = None
    scope = None
    application_type = None
    authorization_code = None
    redirect_URI = None

    ## get_server_wsdl - if True and a newer WSDL is on the server than the local filesystem retrieve it
    def __init__(self, get_server_wsdl = False, debug = False, params = None, tokenResponse=None):
        self.debug = debug
        if debug:
            logging.basicConfig(level=logging.INFO)
            logging.getLogger('suds.client').setLevel(logging.DEBUG)
            logging.getLogger('suds.transport').setLevel(logging.DEBUG)
            logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
            logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)
        else:
            logging.getLogger('suds').setLevel(logging.INFO)

        self.configure_client(get_server_wsdl, params, tokenResponse)

    def configure_client(self, get_server_wsdl, params, tokenResponse):

        ## Read the config information out of config.python
        config = configparser.RawConfigParser()

        if os.path.exists(os.path.expanduser('~/.fuelsdk/config.python')):
            config.read(os.path.expanduser('~/.fuelsdk/config.python'))
        else:
            config.read('config.python')

        if params is not None and 'clientid' in params:
            self.client_id = params['clientid']
        elif config.has_option('Web Services', 'clientid'):
            self.client_id = config.get('Web Services', 'clientid')
        elif 'FUELSDK_CLIENT_ID' in os.environ:
            self.client_id = os.environ['FUELSDK_CLIENT_ID']

        if params is not None and 'clientsecret' in params:
            self.client_secret = params['clientsecret']
        elif config.has_option('Web Services', 'clientsecret'):
            self.client_secret = config.get('Web Services', 'clientsecret')
        elif 'FUELSDK_CLIENT_SECRET' in os.environ:
            self.client_secret = os.environ['FUELSDK_CLIENT_SECRET']

        if params is not None and 'appsignature' in params:
            self.appsignature = params['appsignature']
        elif config.has_option('Web Services', 'appsignature'):
            self.appsignature = config.get('Web Services', 'appsignature')
        elif 'FUELSDK_APP_SIGNATURE' in os.environ:
            self.appsignature = os.environ['FUELSDK_APP_SIGNATURE']

        if params is not None and 'defaultwsdl' in params:
            wsdl_server_url = params['defaultwsdl']
        elif config.has_option('Web Services', 'defaultwsdl'):
            wsdl_server_url = config.get('Web Services', 'defaultwsdl')
        elif 'FUELSDK_DEFAULT_WSDL' in os.environ:
            wsdl_server_url = os.environ['FUELSDK_DEFAULT_WSDL']
        else:
            wsdl_server_url = 'https://webservice.exacttarget.com/etframework.wsdl'

        if params is not None and 'baseapiurl' in params:
            self.base_api_url = params['baseapiurl']
        elif config.has_option('Web Services', 'baseapiurl'):
            self.base_api_url = config.get('Web Services', 'baseapiurl')
        elif 'FUELSDK_BASE_API_URL' in os.environ:
            self.base_api_url = os.environ['FUELSDK_BASE_API_URL']
        else:
            self.base_api_url = 'https://www.exacttargetapis.com'

        if params is not None and 'authenticationurl' in params:
            self.auth_url = params['authenticationurl']
        elif config.has_option('Web Services', 'authenticationurl'):
            self.auth_url = config.get('Web Services', 'authenticationurl')
        elif 'FUELSDK_AUTH_URL' in os.environ:
            self.auth_url = os.environ['FUELSDK_AUTH_URL']

        if params is not None and 'soapendpoint' in params:
            self.soap_endpoint = params['soapendpoint']
        elif config.has_option('Web Services', 'soapendpoint'):
            self.soap_endpoint = config.get('Web Services', 'soapendpoint')
        elif 'FUELSDK_SOAP_ENDPOINT' in os.environ:
            self.soap_endpoint = os.environ['FUELSDK_SOAP_ENDPOINT']

        if params is not None and "wsdl_file_local_loc" in params:
            wsdl_file_local_location = params["wsdl_file_local_loc"]
        elif config.has_option("Web Services", "wsdl_file_local_loc"):
            wsdl_file_local_location = config.get("Web Services", "wsdl_file_local_loc")
        elif "FUELSDK_WSDL_FILE_LOCAL_LOC" in os.environ:
            wsdl_file_local_location = os.environ["FUELSDK_WSDL_FILE_LOCAL_LOC"]
        else:
            wsdl_file_local_location = None

        self.wsdl_file_url = self.load_wsdl(wsdl_server_url, wsdl_file_local_location, get_server_wsdl)

        if params is not None and "useOAuth2Authentication" in params:
            self.use_oAuth2_authentication = params["useOAuth2Authentication"]
        elif config.has_option("Auth Service", "useOAuth2Authentication"):
            self.use_oAuth2_authentication = config.get("Auth Service", "useOAuth2Authentication")
        elif "FUELSDK_USE_OAUTH2" in os.environ:
            self.use_oAuth2_authentication = os.environ["FUELSDK_USE_OAUTH2"]

        if self.is_none_or_empty_or_blank(self.auth_url) == True:
            if self.use_oAuth2_authentication == "True":
                raise Exception('authenticationurl (Auth TSE) is mandatory when using OAuth2 authentication')
            else:
                self.auth_url = 'https://auth.exacttargetapis.com/v1/requestToken?legacy=1'

        if params is not None and "accountId" in params:
            self.account_id = params["accountId"]
        elif config.has_option("Auth Service", "accountId"):
            self.account_id = config.get("Auth Service", "accountId")
        elif "FUELSDK_ACCOUNT_ID" in os.environ:
            self.account_id = os.environ["FUELSDK_ACCOUNT_ID"]

        if params is not None and "scope" in params:
            self.scope = params["scope"]
        elif config.has_option("Auth Service", "scope"):
            self.scope = config.get("Auth Service", "scope")
        elif "FUELSDK_SCOPE" in os.environ:
            self.scope = os.environ["FUELSDK_SCOPE"]

        if params is not None and "authorizationCode" in params:
            self.authorization_code = params["authorizationCode"]
        elif config.has_option("Auth Service", "authorizationCode"):
            self.authorization_code = config.get("Auth Service", "authorizationCode")
        elif "FUELSDK_AUTHORIZATION_CODE" in os.environ:
            self.authorization_code = os.environ["FUELSDK_AUTHORIZATION_CODE"]

        if params is not None and "applicationType" in params:
            self.application_type = params["applicationType"]
        elif config.has_option("Auth Service", "applicationType"):
            self.application_type = config.get("Auth Service", "applicationType")
        elif "FUELSDK_APPLICATION_TYPE" in os.environ:
            self.application_type = os.environ["FUELSDK_APPLICATION_TYPE"]

        if self.is_none_or_empty_or_blank(self.application_type):
            self.application_type = "server"

        if params is not None and "redirectURI" in params:
            self.redirect_URI = params["redirectURI"]
        elif config.has_option("Auth Service", "redirectURI"):
            self.redirect_URI = config.get("Auth Service", "redirectURI")
        elif "FUELSDK_REDIRECT_URI" in os.environ:
            self.redirect_URI = os.environ["FUELSDK_REDIRECT_URI"]

        if self.application_type in ["public", "web"]:
            if self.is_none_or_empty_or_blank(self.authorization_code) or self.is_none_or_empty_or_blank(self.redirect_URI):
                raise Exception('authorizationCode or redirectURI is null: For Public/Web Apps, the authorizationCode and redirectURI must be '
                                'passed when instantiating ET_Client or must be provided in environment variables/config file')

        if self.application_type == "public":
            if self.is_none_or_empty_or_blank(self.client_id):
                raise Exception('clientid is null: clientid must be passed when instantiating ET_Client or must be provided in environment variables / config file')
        else: # application_type is server or web
            if self.is_none_or_empty_or_blank(self.client_id) or self.is_none_or_empty_or_blank(self.client_secret):
                raise Exception('clientid or clientsecret is null: clientid and clientsecret must be passed when instantiating ET_Client '
                                'or must be provided in environment variables / config file')

        ## get the JWT from the params if passed in...or go to the server to get it
        if (params is not None and 'jwt' in params):
            decodedJWT = jwt.decode(params['jwt'], self.appsignature)
            self.authToken = decodedJWT['request']['user']['oauthToken']
            self.authTokenExpiration = time.time() + decodedJWT['request']['user']['expiresIn']
            self.internalAuthToken = decodedJWT['request']['user']['internalOauthToken']
            if 'refreshToken' in decodedJWT:
                self.refreshKey = tokenResponse['request']['user']['refreshToken']
            self.build_soap_client()
            pass
        else:
            self.refresh_token()


    def load_wsdl(self, wsdl_url, wsdl_file_local_location, get_server_wsdl = False):
        """
        retrieve the url of the ExactTarget wsdl...either file: or http:
        depending on if it already exists locally or server flag is set and
        server has a newer copy
        """
        if wsdl_file_local_location is not None:
           file_location = wsdl_file_local_location
        else:
           path = os.path.dirname(os.path.abspath(__file__))
           file_location = os.path.join(path, 'ExactTargetWSDL.xml')
        file_url = 'file:///' + file_location 
        
        if not os.path.exists(file_location) or os.path.getsize(file_location) == 0:   #if there is no local copy or local copy is empty then go get it...
            self.retrieve_server_wsdl(wsdl_url, file_location)
        elif get_server_wsdl:
            r = requests.head(wsdl_url)
            if r is not None and 'last-modified' in r.headers:
                server_wsdl_updated = time.strptime(r.headers['last-modified'], '%a, %d %b %Y %H:%M:%S %Z')
                file_wsdl_updated = time.gmtime(os.path.getmtime(file_location))
                if server_wsdl_updated > file_wsdl_updated:
                    self.retrieve_server_wsdl(wsdl_url, file_location)
            
        return file_url
            

    def retrieve_server_wsdl(self, wsdl_url, file_location):
        """
        get the WSDL from the server and save it locally
        """
        r = requests.get(wsdl_url)
        f = open(file_location, 'w')
        f.write(r.text)
        

    def build_soap_client(self):
        if self.soap_endpoint is None or not self.soap_endpoint:
            self.soap_endpoint = self.get_soap_endpoint()

        self.soap_client = suds.client.Client(self.wsdl_file_url, faults=False, cachingpolicy=1)
        self.soap_client.set_options(location=self.soap_endpoint)
        self.soap_client.set_options(headers={'user-agent' : 'FuelSDK-Python-v1.3.0'})

        if self.use_oAuth2_authentication == 'True':
            element_oAuth = Element('fueloauth', ns=('etns', 'http://exacttarget.com'))
            element_oAuth.setText(self.authToken);
            self.soap_client.set_options(soapheaders=(element_oAuth))
        else:
            element_oAuth = Element('oAuth', ns=('etns', 'http://exacttarget.com'))
            element_oAuthToken = Element('oAuthToken').setText(self.internalAuthToken)
            element_oAuth.append(element_oAuthToken)
            self.soap_client.set_options(soapheaders=(element_oAuth))

            security = suds.wsse.Security()
            token = suds.wsse.UsernameToken('*', '*')
            security.tokens.append(token)
            self.soap_client.set_options(wsse=security)
        

    def refresh_token(self, force_refresh = False):
        """
        Called from many different places right before executing a SOAP call
        """

        if self.use_oAuth2_authentication == "True":
            self.refresh_token_with_oAuth2(force_refresh)
            return

        #If we don't already have a token or the token expires within 5 min(300 seconds), get one
        if (force_refresh or self.authToken is None or (self.authTokenExpiration is not None and time.time() + 300 > self.authTokenExpiration)):
            headers = {'content-type' : 'application/json', 'user-agent' : 'FuelSDK-Python-v1.3.0'}
            if (self.authToken is None):
                payload = {'clientId' : self.client_id, 'clientSecret' : self.client_secret, 'accessType': 'offline'}
            else:
                payload = {'clientId' : self.client_id, 'clientSecret' : self.client_secret, 'refreshToken' : self.refreshKey, 'accessType': 'offline'}
            if self.refreshKey:
                payload['refreshToken'] = self.refreshKey

            legacyString = "?legacy=1"
            if legacyString not in self.auth_url:
                self.auth_url = self.auth_url.strip()
                self.auth_url = self.auth_url + legacyString

            r = requests.post(self.auth_url, data=json.dumps(payload), headers=headers)
            tokenResponse = r.json()
            
            if 'accessToken' not in tokenResponse:
                raise Exception('Unable to validate App Keys(ClientID/ClientSecret) provided: ' + repr(r.json()))
            
            self.authToken = tokenResponse['accessToken']
            self.authTokenExpiration = time.time() + tokenResponse['expiresIn']
            self.internalAuthToken = tokenResponse['legacyToken']
            if 'refreshToken' in tokenResponse:
                self.refreshKey = tokenResponse['refreshToken']
        
            self.build_soap_client()

    def refresh_token_with_oAuth2(self, force_refresh=False):
        """
        Called from many different places right before executing a SOAP call
        """
        # If we don't already have a token or the token expires within 5 min(300 seconds), get one
        if force_refresh or self.authToken is None \
                or self.authTokenExpiration is not None and time.time() + 300 > self.authTokenExpiration:

            headers = {'content-type': 'application/json',
                       'user-agent': 'FuelSDK-Python-v1.3.0'}

            payload = self.create_payload()

            auth_endpoint = self.auth_url.strip() + '/v2/token'

            r = requests.post(auth_endpoint, data=json.dumps(payload), headers=headers)
            tokenResponse = r.json()

            if 'access_token' not in tokenResponse:
                raise Exception('Unable to validate App Keys(ClientID/ClientSecret) provided: ' + repr(r.json()))

            self.authToken = tokenResponse['access_token']
            self.authTokenExpiration = time.time() + tokenResponse['expires_in']
            self.internalAuthToken = tokenResponse['access_token']
            self.soap_endpoint = tokenResponse['soap_instance_url'] + 'service.asmx'
            self.base_api_url = tokenResponse['rest_instance_url']

            if 'refresh_token' in tokenResponse:
                self.refreshKey = tokenResponse['refresh_token']

            self.build_soap_client()

    def create_payload(self):
        payload = {'client_id': self.client_id}

        if self.application_type != "public":
            payload['client_secret'] = self.client_secret

        if not self.is_none_or_empty_or_blank(self.refreshKey):
            payload['grant_type'] = "refresh_token"
            payload['refresh_token'] = self.refreshKey
        elif self.application_type in ["public", "web"]:
            payload['grant_type'] = "authorization_code"
            payload['code'] = self.authorization_code
            payload['redirect_uri'] = self.redirect_URI
        else:
            payload['grant_type'] = "client_credentials"

        if not self.is_none_or_empty_or_blank(self.account_id):
            payload['account_id'] = self.account_id
        if not self.is_none_or_empty_or_blank(self.scope):
            payload['scope'] = self.scope

        return payload

    def get_soap_cache_file(self):
        json_data = {}
        if os.path.isfile(self.soap_cache_file):
            file = open(self.soap_cache_file, "r")
            json_data = json.load(file)
            file.close()

        return json_data

    def update_cache_file(self, url):
        file = open(self.soap_cache_file, "w+")

        data = {}
        data['url'] = url
        data['timestamp'] = time.time() + (10 * 60)
        json.dump(data, file)
        file.close()

    def get_soap_endpoint(self):
        default_endpoint = 'https://webservice.exacttarget.com/Service.asmx'

        cache_file_data = self.get_soap_cache_file()

        if 'url' in cache_file_data and 'timestamp' in cache_file_data \
            and cache_file_data['timestamp'] > time.time():
            return cache_file_data['url']

        """
        find the correct url that data request web calls should go against for the token we have.
        """
        try:
            r = requests.get(self.base_api_url + '/platform/v1/endpoints/soap', headers={
                'user-agent': 'FuelSDK-Python-v1.3.0',
                'authorization': 'Bearer ' + self.authToken
            })

            contextResponse = r.json()
            if ('url' in contextResponse):
                soap_url = str(contextResponse['url'])
                self.update_cache_file(soap_url)
                return soap_url
            else:
                return default_endpoint

        except Exception as e:
            return default_endpoint

    def AddSubscriberToList(self, emailAddress, listIDs, subscriberKey = None):
        """
        add or update a subscriber with a list
        """
        newSub = ET_Subscriber()
        newSub.auth_stub = self
        lists = []
        
        for p in listIDs:
            lists.append({"ID" : p})
        
        newSub.props = {"EmailAddress" : emailAddress, "Lists" : lists}
        if subscriberKey is not None:
            newSub.props['SubscriberKey']  = subscriberKey
        
        # Try to add the subscriber
        postResponse = newSub.post()
        
        if not postResponse.status:
            # If the subscriber already exists in the account then we need to do an update.
            # Update Subscriber On List 
            if postResponse.results[0]['ErrorCode'] == 12014:    
                patchResponse = newSub.patch()
                return patchResponse

        return postResponse
    

    def CreateDataExtensions(self, dataExtensionDefinitions):
        """
        write the data extension props to the web service
        """
        newDEs = ET_DataExtension()
        newDEs.auth_stub = self
                
        newDEs.props = dataExtensionDefinitions                     
        postResponse = newDEs.post()        
        
        return postResponse

    def is_none_or_empty_or_blank(self, str):
        if str and str.strip():
            return False
        return True
