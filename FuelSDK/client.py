import os
import logging
import ConfigParser
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
        
    ## get_server_wsdl - if True and a newer WSDL is on the server than the local filesystem retrieve it
    def __init__(self, get_server_wsdl = False, debug = False, params = None):
        self.debug = debug
        if debug:
            logging.basicConfig(level=logging.INFO)
            logging.getLogger('suds.client').setLevel(logging.DEBUG)
            logging.getLogger('suds.transport').setLevel(logging.DEBUG)
            logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
            logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)

        ## Read the config information out of config.python
        config = ConfigParser.RawConfigParser()
        if os.path.exists(os.path.expanduser('~/.fuelsdk/config.python')):
            config.read(os.path.expanduser('~/.fuelsdk/config.python'))
        else:
            config.read('config.python')

        if config.has_option('Web Services', 'clientid'):
            self.client_id = config.get('Web Services', 'clientid')
        elif 'FUELSDK_CLIENT_ID' in os.environ:
            self.client_id = os.environ['FUELSDK_CLIENT_ID']

        if config.has_option('Web Services', 'clientsecret'):
            self.client_secret = config.get('Web Services', 'clientsecret')
        elif 'FUELSDK_CLIENT_SECRET' in os.environ:
            self.client_secret = os.environ['FUELSDK_CLIENT_SECRET']

        if config.has_option('Web Services', 'appsignature'):
            self.appsignature = config.get('Web Services', 'appsignature')
        elif 'FUELSDK_APP_SIGNATURE' in os.environ:
            self.appsignature = os.environ['FUELSDK_APP_SIGNATURE']

        if config.has_option('Web Services', 'defaultwsdl'):
            wsdl_server_url = config.get('Web Services', 'defaultwsdl')
        elif 'FUELSDK_DEFAULT_WSDL' in os.environ:
            wsdl_server_url = os.environ['FUELSDK_DEFAULT_WSDL']
        else:
            wsdl_server_url = 'https://webservice.exacttarget.com/etframework.wsdl'

        if config.has_option('Web Services', 'authenticationurl'):
            self.auth_url = config.get('Web Services', 'authenticationurl')
        elif 'FUELSDK_AUTH_URL' in os.environ:
            self.auth_url = os.environ['FUELSDK_AUTH_URL']
        else:
            self.auth_url = 'https://auth.exacttargetapis.com/v1/requestToken?legacy=1'

        self.wsdl_file_url = self.load_wsdl(wsdl_server_url, get_server_wsdl)
        
        ## get the JWT from the params if passed in...or go to the server to get it             
        if(params is not None and 'jwt' in params):
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


    def load_wsdl(self, wsdl_url, get_server_wsdl = False):
        """
        retrieve the url of the ExactTarget wsdl...either file: or http:
        depending on if it already exists locally or server flag is set and
        server has a newer copy
        """
        path = os.path.dirname(os.path.abspath(__file__))
        file_location = os.path.join(path, 'ExactTargetWSDL.xml')
        file_url = 'file:///' + file_location 
        
        if not os.path.exists(file_location):   #if there is no local copy then go get it...
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
        if self.endpoint is None: 
            self.endpoint = self.determineStack()
        
        self.authObj = {'oAuth' : {'oAuthToken' : self.internalAuthToken}}          
        self.authObj['attributes'] = { 'oAuth' : { 'xmlns' : 'http://exacttarget.com' }}                        

        self.soap_client = suds.client.Client(self.wsdl_file_url, faults=False, cachingpolicy=1)
        self.soap_client.set_options(location=self.endpoint)

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
        #If we don't already have a token or the token expires within 5 min(300 seconds), get one
        if (force_refresh or self.authToken is None or (self.authTokenExpiration is not None and time.time() + 300 > self.authTokenExpiration)):
            headers = {'content-type' : 'application/json'}
            if (self.authToken is None):
                payload = {'clientId' : self.client_id, 'clientSecret' : self.client_secret, 'accessType': 'offline'}
            else:
                payload = {'clientId' : self.client_id, 'clientSecret' : self.client_secret, 'refreshToken' : self.refreshKey, 'accessType': 'offline', 'scope':'cas:'+ self.internalAuthToken}
            if self.refreshKey:
                payload['refreshToken'] = self.refreshKey

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
            

    def determineStack(self):
        """
        find the correct url that data request web calls should go against for the token we have.
        """
        try:
            r = requests.get('https://www.exacttargetapis.com/platform/v1/endpoints/soap?access_token=' + self.authToken)           
            contextResponse = r.json()
            if('url' in contextResponse):
                return str(contextResponse['url'])

        except Exception as e:
            raise Exception('Unable to determine stack using /platform/v1/tokenContext: ' + e.message)  


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
