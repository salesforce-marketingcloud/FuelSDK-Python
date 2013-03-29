import requests
import suds.client
import suds.wsse
from suds.sax.element import Element
import logging

import os
import ConfigParser
import time
import json

########
##
##    Setup web service connectivity by getting need config data, security tokens etc.
##
########
class ET_Client(object):
    debug = False
    
    client_id = None
    client_secret = None
    appsignature = None

    wsdl_file_url = None
    
    authToken = None
    internalAuthToken = None
    authTokenExpiration = None  #seconds since epoch that the current jwt token will expire
    refreshKey = False
    endpoint = None
    authObj = None
    soap_client = None
        
    ## get_server_wsdl - if True and a newer WSDL is on the server than the local filesystem retrieve it
    def __init__(self, get_server_wsdl = False, debug = False, params = None):
        self.debug = debug
        if(debug):
            logging.basicConfig(level=logging.INFO)
            logging.getLogger('suds.client').setLevel(logging.DEBUG)
            logging.getLogger('suds.transport').setLevel(logging.DEBUG)
            logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
            logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)

        ## Read the config information out of config.python
        config = ConfigParser.RawConfigParser()
        config.read('config.python')
        self.client_id = config.get('Web Services', 'clientid')
        self.client_secret = config.get('Web Services', 'clientsecret')
        self.appsignature = config.get('Web Services', 'appsignature')
        wsdl_server_url = config.get('Web Services', 'defaultwsdl')
        
        try:
            self.wsdl_file_url = self.load_wsdl(wsdl_server_url, get_server_wsdl)
            
            ## get the JWT from the params if passed in...or go to the server to get it                
            if(params is not None and 'jwt' in params):
                #jwt.decode(params['jwt'], "secret")
                pass
            else:
                self.refresh_token()
        except Exception as e:
            print str(e.message)

    ## retrieve the url of the ExactTarget wsdl...either file: or http:
    ## depending on if it already exists locally or server flag is set and
    ## server has a newer copy
    def load_wsdl(self, wsdl_url, get_server_wsdl = False):
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
            
    ### get the WSDL from the server and save it locally
    def retrieve_server_wsdl(self, wsdl_url, file_location):
        r = requests.get(wsdl_url)
        f = open(file_location, 'w')
        f.write(r.text)
        
    ## Called from many different places right before executing a SOAP call
    def refresh_token(self, force_refresh = False):
        #If we don't already have a token or the token expires within 5 min(300 seconds), get one
        if (force_refresh or self.authToken is None or (self.authTokenExpiration is not None and time.time() + 300 > self.authTokenExpiration)):
            try:
                headers = {'content-type' : 'application/json'}
                payload = {'clientId' : self.client_id, 'clientSecret' : self.client_secret}
                if self.refreshKey:
                    payload['refreshToken'] = self.refreshKey            

                r = requests.post('https://auth.exacttargetapis.com/v1/requestToken?legacy=1', data=json.dumps(payload), headers=headers)
                tokenResponse = r.json()
                
                if 'accessToken' not in tokenResponse:
                    raise Exception('Unable to validate App Keys(ClientID/ClientSecret) provided: ' + r.body())
                
                self.authToken = tokenResponse['accessToken']
                self.authTokenExpiration = time.time() + tokenResponse['expiresIn']
                self.internalAuthToken = tokenResponse['legacyToken']
                if 'refreshToken' in tokenResponse:
                    self.refreshKey = tokenResponse['refreshToken']
            
                if self.endpoint is None: 
                    self.endpoint = self.determineStack()
            
                self.authObj = {'oAuth' : {'oAuthToken' : self.internalAuthToken}}            
                self.authObj['attributes'] = { 'oAuth' : { 'xmlns' : 'http://exacttarget.com' }}                        

                ##read the WSDL from the filesystem and 
                ##recreate the suds SOAP client with the updated token information
                ##setting faults=False will return the http code (200 etc.) but any errors will need to be handled in code
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
                
            except Exception as e:
                raise Exception('Unable to validate App Keys(ClientID/ClientSecret) provided: ' + e.message)

    ##find the correct url that data request web calls should go against for the token we have.
    def determineStack(self):
        try:
            r = requests.get('https://www.exacttargetapis.com/platform/v1/endpoints/soap?access_token=' + self.authToken)            
            contextResponse = r.json()
            if('url' in contextResponse):
                return str(contextResponse['url'])

        except Exception as e:
            raise Exception('Unable to determine stack using /platform/v1/tokenContext: ' + e.message)  

    ##add or update a subscriber with a list
    def AddSubscriberToList(self, emailAddress, listIDs, subscriberKey = None):
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
    
    ##write the data extension props to the web service
    def CreateDataExtensions(self, dataExtensionDefinitions):
        newDEs = ET_DataExtension()
        newDEs.auth_stub = self
                
        newDEs.props = dataExtensionDefinitions                        
        postResponse = newDEs.post()        
        
        return postResponse
    
########
##
##    Parent class used to determine what status we are in depending on web service call results
##
########
class ET_Constructor(object):
    results = []
    code = None
    status = False
    message = None
    more_results = False                
    request_id = None
    
    def __init__(self, response = None, rest = False):
        
        if response is not None:    #if a response was returned from the web service call
            if rest:    # result is from a REST web service call...
                self.code = response.status_code            
                if self.code == 200:
                    self.status = True
                else:
                    self.status = False 
                        
                try:
                    self.results = response.json()
                except:
                    self.message = response.json()
                
                #additional parsing will happen in the child object that called in to here.
                
            else:   #soap call
                self.code = response[0] #suds puts the code in tuple position 0
                body = response[1]  #and the result in tuple position 1

                # Store the Last Request ID for use with continue
                if 'RequestID' in body:
                    self.request_id = body['RequestID']

                if self.code == 200:
                    self.status = True

                    if 'OverallStatus' in body:
                        self.message = body['OverallStatus']
                        if body['OverallStatus'] == "MoreDataAvailable":
                            self.more_results = True
                        elif body['OverallStatus'] != "OK":
                            self.status = False    
        
                    body_container_tag = None
                    if 'Results' in body:   #most SOAP responses are wrapped in 'Results'
                        body_container_tag = 'Results'
                    elif 'ObjectDefinition' in body:   #Describe SOAP response is in 'ObjectDefinition'
                        body_container_tag = 'ObjectDefinition'
                        
                    if body_container_tag is not None:
                        self.results = body[body_container_tag]                    

                else:
                    self.status = False
                    
    def parse_props_dict_into_ws_object(self, obj_type, ws_object, props_dict):
        for k, v in props_dict.iteritems():
            if k in ws_object:
                ws_object[k] = v
            else:
                message = k + ' is not a property of ' + obj_type
                print message
                raise Exception(message)
        return ws_object

    def parse_props_into_ws_object(self, auth_stub, obj_type, props):
        if props is not None and type(props) is dict:
            ws_create = auth_stub.soap_client.factory.create(obj_type)
            ws_create = self.parse_props_dict_into_ws_object(obj_type, ws_create, props)
            return ws_create            
        elif props is not None and type(props) is list:
            ws_create_list = []
            for prop_dict in props:
                ws_create = auth_stub.soap_client.factory.create(obj_type)
                ws_create = self.parse_props_dict_into_ws_object(obj_type, ws_create, prop_dict)
                ws_create_list.append(ws_create)
            return ws_create_list
        else:
            message = 'Can not post properties to ' + obj_type + ' without a dict or list of properties'
            print message
            raise Exception(message)        
        
########
##
##    Used to Describe Objects via web service call
##
########
class ET_Describe(ET_Constructor):
    def __init__(self, auth_stub, obj_type):        
        auth_stub.refresh_token()

        ws_describeRequest = auth_stub.soap_client.factory.create('ArrayOfObjectDefinitionRequest')

        ObjectDefinitionRequest = { 'ObjectType' : obj_type}
        ws_describeRequest.ObjectDefinitionRequest = [ObjectDefinitionRequest]

        response = auth_stub.soap_client.service.Describe(ws_describeRequest)        

        if response is not None:
            self.message = 'Describe: ' + obj_type
            super(ET_Describe, self).__init__(response)

########
##
##    Get call to a web service
##
########
class ET_Get(ET_Constructor):
    def __init__(self, auth_stub, obj_type, props = None, search_filter = None):        
        auth_stub.refresh_token()
        
        if props is None:   #if there are no properties to retrieve for the obj_type then return a Description of obj_type
            describe = ET_Describe(auth_stub, obj_type)
            self.results = describe.results
            self.code = describe.code
            self.status = describe.status
            self.message = describe.message
            self.more_results = describe.more_results                
            self.request_id = describe.request_id
            return

        ws_retrieveRequest = auth_stub.soap_client.factory.create('RetrieveRequest')
                
        if props is not None:
            if type(props) is dict: # If the properties is a hash, then we just want to use the keys
                ws_retrieveRequest.Properties = props.keys
            else:
                ws_retrieveRequest.Properties = props

        if search_filter is not None:
            ws_simpleFilterPart = auth_stub.soap_client.factory.create('SimpleFilterPart')
            
            for prop in ws_simpleFilterPart:
                if prop[0] in search_filter:
                    ws_simpleFilterPart[prop[0]] = search_filter[prop[0]]
           
            ws_retrieveRequest.Filter = ws_simpleFilterPart

        ws_retrieveRequest.ObjectType = obj_type
        
        response = auth_stub.soap_client.service.Retrieve(ws_retrieveRequest)        

        if response is not None:
            super(ET_Get, self).__init__(response)

########
##
##    Call the Exact Target web service Create method
##
########
class ET_Post(ET_Constructor):
    def __init__(self, auth_stub, obj_type, props = None):
        auth_stub.refresh_token()

        response = auth_stub.soap_client.service.Create(None, self.parse_props_into_ws_object(auth_stub, obj_type, props))
        if(response is not None):
            super(ET_Post, self).__init__(response)

########
##
##    Call the Exact Target web service Update method
##
########
class ET_Patch(ET_Constructor):
    def __init__(self, auth_stub, obj_type, props = None):
        auth_stub.refresh_token()
              
        response = auth_stub.soap_client.service.Update(None, self.parse_props_into_ws_object(auth_stub, obj_type, props))

        if(response is not None):
            super(ET_Patch, self).__init__(response)

########
##
##    Call the Exact Target web service Delete method
##
########
class ET_Delete(ET_Constructor):
    def __init__(self, auth_stub, obj_type, props = None):
        auth_stub.refresh_token()
              
        response = auth_stub.soap_client.service.Delete(None, self.parse_props_into_ws_object(auth_stub, obj_type, props))

        if(response is not None):
            super(ET_Delete, self).__init__(response)

########
##
##    Call the Exact Target web service RetrieveRequest passing in ContinueRequest param
##
########
class ET_Continue(ET_Constructor):
    def __init__(self, auth_stub, request_id):
        auth_stub.refresh_token()

        ws_continueRequest = auth_stub.soap_client.factory.create('RetrieveRequest')
        ws_continueRequest.ContinueRequest = request_id
        response = auth_stub.soap_client.service.Retrieve(ws_continueRequest)        

        if response is not None:
            super(ET_Continue, self).__init__(response)

########
##
##    set up variables for children objects to share
##
########
class ET_BaseObject(object):
    auth_stub = None
    obj = None
    last_request_id = None
    endpoint = None
    props = None
    extProps = None
    search_filter = None

########
##
##    make sure needed information is available and then make the call to ET_Get to call the webservice
##
########
class ET_GetSupport(ET_BaseObject):
    obj_type = 'ET_GetSupport'   #should be overwritten by inherited class
    
    def get(self, m_props = None, m_filter = None):
        props = self.props
        search_filter = self.search_filter
        
        if m_props is not None and type(m_props) is list:
            props = m_props        
        elif self.props is not None and type(self.props) is dict:
            props = self.props.keys()

        if m_filter is not None and type(m_filter) is dict:
            search_filter = m_filter

        obj = ET_Get(self.auth_stub, self.obj_type, props, search_filter)
        if obj is not None:
            self.last_request_id = obj.request_id
        return obj
    
    def info(self):
        obj = ET_Describe(self.auth_stub, self.obj_type)
        if obj is not None:
            self.last_request_id = obj.request_id
        return obj
    
    def getMoreResults(self):
        obj = ET_Continue(self.auth_stub, self.last_request_id)
        if obj is not None:
            self.last_request_id = obj.request_id
        return obj

########
##
##    Restful webservice to Get data
##
########
class ET_GetRest(ET_Constructor):
    def __init__(self, auth_stub, endpoint, qs = None):
        auth_stub.refresh_token()    

        r = requests.get(endpoint + '?access_token=' + auth_stub.authToken)        
        
        self.more_results = False
                    
        obj = super(ET_GetRest, self).__init__(r, True)
        return obj

########
##
##    Restful webservice to Get data
##
########
class ET_PostRest(ET_Constructor):    
    def __init__(self, auth_stub, endpoint, payload):
        auth_stub.refresh_token()
        
        headers = {'content-type' : 'application/json'}
        r = requests.post(endpoint + '?access_token=' + auth_stub.authToken , data=json.dumps(payload), headers=headers)
        
        obj = super(ET_PostRest, self).__init__(r, True)
        return obj
    
########
##
##    Restful webservice to Get data
##
########
class ET_PatchRest(ET_Constructor):
    def __init__(self, auth_stub, endpoint, payload):
        auth_stub.refresh_token()
        
        headers = {'content-type' : 'application/json'}
        r = requests.patch(endpoint + '?access_token=' + auth_stub.authToken , data=json.dumps(payload), headers=headers)
        
        obj = super(ET_PatchRest, self).__init__(r, True)
        return obj

########
##
##    Restful webservice to Get data
##
########
class ET_DeleteRest(ET_Constructor):
    def __init__(self, auth_stub, endpoint):
        auth_stub.refresh_token()
        
        r = requests.delete(endpoint + '?access_token=' + auth_stub.authToken)
        
        obj = super(ET_DeleteRest, self).__init__(r, True)
        return obj

########
##
##    Get data
##
########
class ET_CUDSupport(ET_GetSupport):
    
    def __init__(self):
        super(ET_CUDSupport, self).__init__()
        
    def post(self):
        if self.extProps is not None:
            for k, v in self.extProps.iteritems():
                self.props[k.capitalize] = v
        
        obj = ET_Post(self.auth_stub, self.obj_type, self.props)
        if obj is not None:
            self.last_request_id = obj.request_id
        return obj
    
    def patch(self):
        obj = ET_Patch(self.auth_stub, self.obj_type, self.props)
        if obj is not None:
            self.last_request_id = obj.request_id
        return obj

    def delete(self):
        obj = ET_Delete(self.auth_stub, self.obj_type, self.props)
        if obj is not None:
            self.last_request_id = obj.request_id
        return obj

########
##
##    Get data using a REST call
##
########
class ET_GetSupportRest(ET_BaseObject):
    urlProps = None
    urlPropsRequired = None
    lastPageNumber = None
    
    def __init__(self):
        super
    
    def get(self, props = None):
        if props is not None and type(props) is dict:
            self.props = props
            
        completeURL = self.endpoint        
        additionalQS = {}
        
        if self.props is not None and type(self.props) is dict:
            for k, v in self.props.iteritems():
                if k in self.urlProps:
                    completeURL = completeURL.replace('{{{0}}}'.format(k), v)
                else:
                    additionalQS[k] = v
        
        for value in self.urlPropsRequired: 
            if self.props is None or value not in self.props:
                raise "Unable to process request due to missing required prop: #{value}"
        
        for value in self.urlProps:             
            completeURL = completeURL.replace('/{{{0}}}'.format(value), '')

        obj = ET_GetRest(self.auth_stub, completeURL, additionalQS)    
        
        results = obj.results
        print type(results)
        if 'page' in obj.results: 
            self.lastPageNumber = obj.results['page']
            pageSize = obj.results['pageSize']
            if 'count' in obj.results: 
                count = obj.results['count']
            elif 'totalCount' in obj.results: 
                count = obj.results['totalCount']
                    
            if count is not None and count > (self.lastPageNumber * pageSize):
                obj.more_results = True    
            
        return obj
    
    def getMoreResults(self):
        props = None    #where should it come from?
        if props is not None and type(props) is dict:
            self.props = props
        
        originalPageValue = "1"
        removePageFromProps = False            
        
        if self.props is not None and '$page' in self.props: 
            originalPageValue = self.props['page']
        else:
            removePageFromProps = True 
        
        if self.props is None:
            self.props = {}
        
        self.props['$page'] = self.lastPageNumber + 1
        
        obj = self.get
        
        if removePageFromProps:
            del self.props.delete['$page']
        else:
            self.props['$page'] = originalPageValue
        
        return obj

########
##
##    Create, Update and Delete using a REST call
##
########            
class ET_CUDSupportRest(ET_GetSupportRest):
    endpoint = None
    urlProps = None
    urlPropsRequired = None
    
    def __init__(self):
        super
    
    def post(self):
        completeURL = self.endpoint    
        
        if self.props is not None and type(self.props) is dict:
            for k, v in self.props.iteritems():
                if k in self.urlProps:
                    completeURL = completeURL.replace('{{{0}}}'.format(k), v)
        
        for value in self.urlPropsRequired: 
            if self.props is None or value not in self.props:
                raise "Unable to process request due to missing required prop: #{value}"

        # Clean Optional Parameters from Endpoint URL first 
        for value in self.urlProps:             
            completeURL = completeURL.replace('/{{{0}}}'.format(value), '')         

        obj = ET_PostRest(self.auth_stub, completeURL, self.props)
        return obj        
    
    def patch(self):
        completeURL = self.endpoint
        # All URL Props are required when doing Patch    
        for value in self.urlProps: 
            if self.props is None or value not in self.props:
                raise "Unable to process request due to missing required prop: #{value}"
        
        if self.props is not None and type(self.props) is dict:
            for k, v in self.props.iteritems():
                if k in self.urlProps:
                    completeURL = completeURL.replace('{{{0}}}'.format(k), v)
        
        obj = ET_PatchRest(self.auth_stub, completeURL, self.props)            
        return obj
    
    def delete(self):
        completeURL = self.endpoint        
        # All URL Props are required when doing Patch    
        for value in self.urlProps: 
            if self.props is None or value not in self.props:
                raise "Unable to process request due to missing required prop: #{value}"
        
        if self.props is not None and type(self.props) is dict:        
            for k, v in self.props.iteritems():
                if k in self.urlProps:
                    completeURL = completeURL.replace('{{{0}}}'.format(k), v)

        obj = ET_DeleteRest(self.auth_stub, completeURL)
        return obj

########
##
##    wrap an Exact Target Content Area
##
########
class ET_ContentArea(ET_CUDSupport):    
    def __init__(self):
        super(ET_ContentArea, self).__init__()
        self.obj_type = 'ContentArea'

########
##
##    wrap an Exact Target Bounce Event
##
########
class ET_BounceEvent(ET_GetSupport):
    def __init__(self):
        self.obj_type = 'BounceEvent'
     
########
##
##    wrap an Exact Target Campaign and associated Assets
##
########        
class ET_Campaign(ET_CUDSupportRest):
    def __init__(self):
        super(ET_Campaign, self).__init__()
        self.endpoint = 'https://www.exacttargetapis.com/hub/v1/campaigns/{id}'
        self.urlProps = ["id"]
        self.urlPropsRequired = []
        
    ##the patch rest service is not implemented for campaigns yet.  use post instead and remove this when patch is implemented on the back end
    def patch(self):
        self.endpoint = 'https://www.exacttargetapis.com/hub/v1/campaigns'  #don't put the id on the url when patching via post
        obj = super(ET_Campaign, self).post()
        self.endpoint = 'https://www.exacttargetapis.com/hub/v1/campaigns/{id}' #but set it back to the url with id for other operations to continue working
        return obj
    
class ET_Campaign_Asset(ET_CUDSupportRest):
    def __init__(self):
        super(ET_Campaign_Asset, self).__init__()
        self.endpoint = 'https://www.exacttargetapis.com/hub/v1/campaigns/{id}/assets/{assetId}'
        self.urlProps = ["id", "assetId"]
        self.urlPropsRequired = ["id"]
        
########
##
##    wrap an Exact Target Click Event
##
########
class ET_ClickEvent(ET_GetSupport):
    def __init__(self):
        super(ET_ClickEvent, self).__init__()
        self.obj_type = 'ClickEvent'
        
########
##
##    wrap an Exact Target List and List Subscriber
##
########
class ET_List(ET_CUDSupport):
    def __init__(self):
        super(ET_List, self).__init__()
        self.obj_type = 'List'
    
class ET_List_Subscriber(ET_GetSupport):
    def __init__(self):
        super(ET_List_Subscriber, self).__init__()
        self.obj_type = 'ListSubscriber'    









class ET_SentEvent(ET_GetSupport):
    def __init__(self):
        super(ET_SentEvent, self).__init__()
        self.obj_type = 'SentEvent'

class ET_OpenEvent(ET_GetSupport):
    def __init__(self):
        super(ET_OpenEvent, self).__init__()
        self.obj_type = 'OpenEvent'

class ET_UnsubEvent(ET_GetSupport):
    def __init__(self):
        super(ET_UnsubEvent, self).__init__()
        self.obj_type = 'UnsubEvent'

class ET_Email(ET_CUDSupport):
    def __init__(self):
        super(ET_Email, self).__init__()
        self.obj_type = 'Email'

class ET_TriggeredSend(ET_CUDSupport):
    subscribers = None
    
    def __init__(self):
        super(ET_TriggeredSend, self).__init__()
        self.obj_type = 'TriggeredSendDefinition'

    def send(self):
        tscall = {"TriggeredSendDefinition" : self.props, "Subscribers" : self.subscribers}
        self.obj = ET_Post(self.auth_stub, "TriggeredSend", tscall)
        return self.obj


class ET_Subscriber(ET_CUDSupport):
    def __init__(self):
        super(ET_Subscriber, self).__init__()
        self.obj_type = 'Subscriber'
        
class ET_DataExtension(ET_CUDSupport):
    columns = None
    
    def __init__(self):
        super(ET_DataExtension, self).__init__()
        self.obj_type = 'DataExtension'    
    
    def post(self):
        originalProps = self.props

        if type(self.props) is list:
            multiDE = []
            for currentDE in self.props:
                currentDE['Fields'] = {}
                currentDE['Fields']['Field'] = []                
                for key in currentDE['columns']:                    
                    currentDE['Fields']['Field'].append(key)
                del currentDE['columns']
                multiDE.append(currentDE.copy())
        
            self.props = multiDE
        else:
            self.props['Fields'] = {}
            self.props['Fields']['Field'] = []
            
            for key in self.columns:        
                self.props['Fields']['Field'].append(key)
        
        obj = super(ET_DataExtension, self).post()
        self.props = originalProps    
        return obj

    def patch(self):
        self.props['Fields'] = {}
        self.props['Fields']['Field'] = []
        for key in self.columns:
            self.props['Fields']['Field'].append(key)
        obj = super(ET_DataExtension, self).patch()
        del self.props["Fields"]         
        return obj
    
class ET_DataExtension_Column(ET_GetSupport):
    def __init__(self):
        super(ET_DataExtension_Column, self).__init__()
        self.obj = 'DataExtensionField'
        
    def get(self):
        '''
        if props and props.is_a? Array then
            @props = props
        end
        '''
        
        if self.props is not None and type(self.props) is dict:
            self.props = self.props.keys()

        '''
        if filter and filter.is_a? Hash then
            @filter = filter
        end
        '''
                
        '''                
        fixCustomerKey = False
        if filter and filter.is_a? Hash then
            @filter = filter
            if @filter.has_key?("Property") && @filter["Property"] == "CustomerKey" then
                @filter["Property"]  = "DataExtension.CustomerKey"
                fixCustomerKey = true 
            end 
        end
        '''
        
        obj = ET_Get(self.auth_stub, self.obj, self.props, self.search_filter)                        
        self.last_request_id = obj.request_id    
        
        '''    
        if fixCustomerKey then
            @filter["Property"] = "CustomerKey"
        end 
        '''
            
        return obj

class ET_DataExtension_Row(ET_CUDSupport):
    Name = None
    CustomerKey = None        
                
    def __init__(self):                                
        super(ET_DataExtension_Row, self).__init__()
        self.obj_type = "DataExtensionObject"
        
    def get(self):
        self.getName()
        '''
        if props and props.is_a? Array then
            @props = props
        end
        '''
        
        if self.props is not None and type(self.props) is dict:
            self.props = self.props.keys()

        '''
        if filter and filter.is_a? Hash then
            @filter = filter
        end
        '''
            
        obj = ET_Get(self.auth_stub, "DataExtensionObject[{0}]".format(self.Name), self.props, self.search_filter)                        
        self.last_request_id = obj.request_id                
            
        return obj
        
    def post(self):
        self.getCustomerKey()
        originalProps = self.props
        
        ## FIX THIS
        if type(self.props) is list:
            pass    ##THIS SHOULD DO SOMETHING
        else:
            currentFields = []
            currentProp = {}
                
            for key, value in self.props.iteritems():
                currentFields.append({"Name" : key, "Value" : value})

            currentProp['CustomerKey'] = self.CustomerKey
            currentProp['Properties'] = {}
            currentProp['Properties']['Property'] = currentFields    

        obj = ET_Post(self.auth_stub, self.obj_type, currentProp)    
        self.props = originalProps
        return obj
        
    def patch(self): 
        self.getCustomerKey()
        currentFields = []
        currentProp = {}
            
        for key, value in self.props.iteritems():
            currentFields.append({"Name" : key, "Value" : value})

        currentProp['CustomerKey'] = self.CustomerKey
        currentProp['Properties'] = {}
        currentProp['Properties']['Property'] = currentFields                                    
            
        obj = ET_Patch(self.auth_stub, self.obj_type, currentProp)
        return obj
    
    def delete(self): 
        self.getCustomerKey()
        currentFields = []
        currentProp = {}
            
        for key, value in self.props.iteritems():
            currentFields.append({"Name" : key, "Value" : value})

        currentProp['CustomerKey'] = self.CustomerKey
        currentProp['Keys'] = {}
        currentProp['Keys']['Key'] = currentFields                                    
            
        obj = ET_Delete(self.auth_stub, self.obj_type, currentProp)
        return obj
    
    def getCustomerKey(self):
        if self.CustomerKey is None:
            if self.Name is None:     
                raise Exception('Unable to process DataExtension::Row request due to CustomerKey and Name not being defined on ET_DatExtension::row')    
            else:
                de = ET_DataExtension()
                de.auth_stub = self.auth_stub
                de.props = ["Name","CustomerKey"]
                de.search_filter = {'Property' : 'CustomerKey','SimpleOperator' : 'equals','Value' : self.Name}
                getResponse = de.get()
                if getResponse.status and len(getResponse.results) == 1 and 'CustomerKey' in getResponse.results[0]: 
                    self.CustomerKey = getResponse.results[0]['CustomerKey']
                else:
                    raise Exception('Unable to process DataExtension::Row request due to unable to find DataExtension based on Name')
                    
                
    def getName(self):
        if self.Name is None:
            if self.CustomerKey is None:
                raise Exception('Unable to process DataExtension::Row request due to CustomerKey and Name not being defined on ET_DatExtension::row')    
            else:
                de = ET_DataExtension()
                de.auth_stub = self.auth_stub
                de.props = ["Name","CustomerKey"]
                de.search_filter = {'Property' : 'CustomerKey','SimpleOperator' : 'equals','Value' : self.CustomerKey}
                getResponse = de.get()
                if getResponse.status and len(getResponse.results) == 1 and 'Name' in getResponse.results[0]: 
                    self.Name = getResponse.results[0]['Name']
                else:
                    raise Exception('Unable to process DataExtension::Row request due to unable to find DataExtension based on CustomerKey')                    