import requests
import suds.client
import suds.wsse
from suds.sax.element import Element
import jwt
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
    wsdl = None
    
    path = None
    
    authToken = None
    internalAuthToken = None
    authTokenExpiration = None  #seconds since epoch that the current jwt token will expire
    refreshKey = False
    endpoint = None
    authObj = None
    soap_client = None
        
    def __init__(self, get_wsdl = False, debug = False, params = None):
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
        self.wsdl = config.get('Web Services', 'defaultwsdl')
        
        try:
            self.path = os.path.dirname(os.path.abspath(__file__))
            
            if(get_wsdl):
                pass    #get the wsdl from the server
                
            ## get the JWT from the params if passed in...or go to the server to get it                
            if(params is not None and 'jwt' in params):
                #jwt.decode(params['jwt'], "secret")
                pass
            else:
                self.refresh_token()
        except Exception as e:
            print e.message

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
                self.soap_client = suds.client.Client('file:///' + os.path.join(self.path, 'ExactTargetWSDL.xml'), faults=False)
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
    body = None
    more_results = False                
    request_id = None
    
    def __init__(self, response = None, rest = False):
        if response is not None and not rest:   #soap call
            self.code = response[0] #suds puts the code in tuple position 0
            self.body = response[1]  
            
            if self.code == 200:
                self.status = True
            else:
                self.status = False            
        elif response is not None:  #rest call
            self.code = response.status_code            
            if self.code == 200:
                self.status = True
            else:
                self.status = False 
                        
            try:
                self.results = response.json()
            except:
                self.message = response.json()

########
##
##    Used to Describe Objects via web service call
##
########
class ET_Describe(ET_Constructor):
    def __init__(self, authStub, objType = None):
        status = False
        body = [0][0]
        try:
            authStub.refresh_token()
            print authStub.soap_client
            arrayOfObjectDefinitionRequest = authStub.soap_client.factory.create('ArrayOfObjectDefinitionRequest')
            print arrayOfObjectDefinitionRequest
            objectDefinitionRequest = authStub.soap_client.factory.create('ObjectDefinitionRequest')
            print objectDefinitionRequest
            response = authStub.soap_client.service.Describe({'DescribeRequests' : {'ObjectDefinitionRequest' : {'ObjectType' : objType} } } )                
        finally:
            if response is not None:
                super(response)
            
            if status:
                objDef = body['definition_response_msg']['object_definition']
                
                s1 = None
                if objDef:
                    s1 = True
                else:
                    s1 = False
                overallStatus = s1
                results = body['definition_response_msg']['object_definition']['properties']            

########
##
##    Get call to a web service
##
########
class ET_Get(ET_Constructor):
    def __init__(self, authStub, objType, props = None, search_filter = None):        
        authStub.refresh_token()
        if props is None:
            resp = ET_Describe(authStub, objType)
            if resp:
                props = []
                '''
                resp.results.map { |p|
                    if p[:is_retrievable] then
                        props << p[:name]
                    end
                }
                '''
                
        ws_retrieveRequest = authStub.soap_client.factory.create('RetrieveRequest')
                
        if props is not None:
            if type(props) is dict: # If the properties is a hash, then we just want to use the keys
                obj = {'ObjectType' : objType, 'Properties' : props.keys}
            else:
                obj = {'ObjectType' : objType, 'Properties' : props}
            ws_retrieveRequest.Properties = props
            
        if search_filter is not None:
            obj['Filter'] = search_filter
            obj['attributes'] = { 'Filter' : { 'xsi:type' : 'tns:SimpleFilterPart' } }
            ws_simpleFilterPart = authStub.soap_client.factory.create('SimpleFilterPart')
            
            for prop in ws_simpleFilterPart:
                if prop[0] in search_filter:
                    ws_simpleFilterPart[prop[0]] = search_filter[prop[0]]
           
            ws_retrieveRequest.Filter = ws_simpleFilterPart

        ws_retrieveRequest.ObjectType = objType
        
        response = authStub.soap_client.service.Retrieve(ws_retrieveRequest)        

        if response is not None:
            super(ET_Get, self).__init__(response)

        if self.status:
            if self.body['OverallStatus'] != "OK" and self.body['OverallStatus'] != "MoreDataAvailable":
                self.status = False    
                self.message = self.body['OverallStatus']
                        
            if self.body['OverallStatus'] == "MoreDataAvailable":
                self.more_results = True                                         
            
            if 'Results' in self.body:
                self.results = self.body['Results']
            
            # Store the Last Request ID for use with continue
            self.request_id = self.body['RequestID']

########
##
##    Call the Exact Target web service Create method
##
########
class ET_Post(ET_Constructor):
    def __init__(self, authStub, objType, props = None):
        authStub.refresh_token()
              
        ws_create = authStub.soap_client.factory.create(objType)
            
        if props is not None and type(props) is dict:
            for k, v in props.iteritems():
                if k in ws_create:
                    ws_create[k] = v
                else:
                    message = k + ' is not a property of ' + objType
                    print message
                    raise Exception(message)
        else:
            message = 'Can not post properties to ' + objType + ' without a dict of properties'
            print message
            raise Exception(message)
        
        response = authStub.soap_client.service.Create(None, ws_create)
             
        if(response is not None):
            super(ET_Post, self).__init__(response)
            
        if self.status:
            if self.body['OverallStatus'] != "OK" and self.body['OverallStatus'] != "MoreDataAvailable":
                self.status = False    
                self.message = self.body['OverallStatus']
                        
            if self.body['OverallStatus'] == "MoreDataAvailable":
                self.more_results = True                                         
            
            if 'Results' in self.body:
                if type(self.body['Results']) is list and len(self.body['Results']) == 1:
                    self.results = self.body['Results'][0]
                else:
                    self.results = self.body['Results']
            
            # Store the Last Request ID for use with continue
            self.request_id = self.body['RequestID']

            '''
                if @@body[:create_response][:overall_status] != "OK"                
                    @status = false
                end 
                
                #@results = @@body[:create_response][:results]
                if !@@body[:create_response][:results].nil? then
                    if !@@body[:create_response][:results].is_a? Hash then
                        @results = @results + @@body[:create_response][:results]
                    else 
                        @results.push(@@body[:create_response][:results])
            '''

########
##
##    Call the Exact Target web service Update method
##
########
class ET_Patch(ET_Constructor):
    def __init__(self, authStub, objType, props = None):
        authStub.refresh_token()
              
        ws_update = authStub.soap_client.factory.create(objType)
            
        if props is not None and type(props) is dict:
            for k, v in props.iteritems():
                if k in ws_update:
                    ws_update[k] = v
                else:
                    message = k + ' is not a property of ' + objType
                    print message
                    raise Exception(message)
        else:
            message = 'Can not post properties to ' + objType + ' without a dict of properties'
            print message
            raise Exception(message)
        
        response = authStub.soap_client.service.Update(None, ws_update)
             
        if(response is not None):
            super(ET_Patch, self).__init__(response)
            
        if self.status:
            if self.body['OverallStatus'] != "OK" and self.body['OverallStatus'] != "MoreDataAvailable":
                self.status = False    
                self.message = self.body['OverallStatus']
                        
            if self.body['OverallStatus'] == "MoreDataAvailable":
                self.more_results = True                                         
            
            if 'Results' in self.body:
                self.results = self.body['Results']
            
            # Store the Last Request ID for use with continue
            self.request_id = self.body['RequestID']

########
##
##    Call the Exact Target web service Delete method
##
########
class ET_Delete(ET_Constructor):
    def __init__(self, authStub, objType, props = None):
        authStub.refresh_token()
              
        ws_delete = authStub.soap_client.factory.create(objType)
            
        if props is not None and type(props) is dict:
            for k, v in props.iteritems():
                if k in ws_delete:
                    ws_delete[k] = v
                else:
                    message = k + ' is not a property of ' + objType
                    print message
                    raise Exception(message)
        else:
            message = 'Can not post properties to ' + objType + ' without a dict of properties'
            print message
            raise Exception(message)
        
        response = authStub.soap_client.service.Delete(None, ws_delete)
             
        if(response is not None):
            super(ET_Delete, self).__init__(response)
            
        if self.status:
            if self.body['OverallStatus'] != "OK" and self.body['OverallStatus'] != "MoreDataAvailable":
                self.status = False    
                self.message = self.body['OverallStatus']
                        
            if self.body['OverallStatus'] == "MoreDataAvailable":
                self.more_results = True                                         
            
            if 'Results' in self.body:
                self.results = self.body['Results']
            
            # Store the Last Request ID for use with continue
            self.request_id = self.body['RequestID']

########
##
##    Call the Exact Target web service Continue method...probably just reuse Get with a flag for continue??
##
########
class ET_Continue(ET_Constructor):
    def __init__(self, authStub, request_id):
        status = None
        results = []
        body = [0][0]
        authStub.refresh_token()    
        obj = {'ContinueRequest' : request_id}        
        response = authStub.soap_client.call('retrieve', {'message' : {'RetrieveRequest' : obj}})                    

        super(response)

        if status:
            if body['retrieve_response_msg']['overall_status'] != "OK" and body['retrieve_response_msg']['overall_status'] != "MoreDataAvailable":
                status = False    
                message = body['retrieve_response_msg']['overall_status']                            

            moreResults = False                
            if body['retrieve_response_msg']['overall_status'] == "MoreDataAvailable":
                moreResults = True
            
            if (type(body['retrieve_response_msg']['results']) is not dict and body['retrieve_response_msg']['results'] is not None):
                results = results + body['retrieve_response_msg']['results']
            elif  (body['retrieve_response_msg']['results'] is not None):
                results.push(body['retrieve_response_msg']['results'])

            # Store the Last Request ID for use with continue
            request_id = body['retrieve_response_msg']['request_id']

########
##
##    set up variables for children objects to share
##
########
class ET_BaseObject(object):
    authStub = None
    obj = None
    lastRequestID = None
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
    objType = 'ET_GetSupport'   #should be overwritten by inherited class
    
    def get(self, m_props = None, m_filter = None):
        props = self.props
        search_filter = self.search_filter
        
        if m_props is not None and type(m_props) is list:
            props = m_props        
        elif self.props is not None and type(self.props) is dict:
            props = self.props.keys()

        if m_filter is not None and type(m_filter) is dict:
            search_filter = m_filter

        obj = ET_Get(self.authStub, self.objType, props, search_filter)
        return obj
    
    def info(self):
        authStub = None;
        obj = None;
        obj = ET_Describe(authStub, obj)
    
    def getMoreResults(self):
        obj = ET_Continue(self.authStub, self.request_id)
        return obj

########
##
##    Restful webservice to Get data
##
########
class ET_GetRest(ET_Constructor):
    def __init__(self, authStub, endpoint, qs = None):
        authStub.refresh_token()    
        
        '''
        if qs is not None: 
            qs['access_token'] = authStub.authToken
        else:
            qs = {"access_token" : authStub.authToken}
        
        r = requests.get(endpoint, data=qs)    #this adds it to the body instead of the url...possibly should work anyway or param to put it in url instead of body??
        '''
        r = requests.get(endpoint + '?access_token=' + authStub.authToken)        
        
        self.more_results = False
                    
        obj = super(ET_GetRest, self).__init__(r, True)
        return obj

########
##
##    Restful webservice to Get additional records to initial request
##
########        
class ET_ContinueRest(ET_Constructor):
    '''
    def initialize(authStub, endpoint, qs = nil)
        authStub.refresh_token()    
        
        if qs then 
            qs['access_token'] = authStub.authToken
        else 
            qs = {"access_token" => authStub.authToken}
        end         
        
        uri = URI.parse(endpoint)
        uri.query = URI.encode_www_form(qs)
        http = Net::HTTP.new(uri.host, uri.port)
        http.use_ssl = true
        request = Net::HTTP::Get.new(uri.request_uri)        
        requestResponse = http.request(request)
        
        @moreResults = false
                    
        super(requestResponse, true)
    '''
    
########
##
##    Restful webservice to Get data
##
########
class ET_PostRest(ET_Constructor):    
    def __init__(self, authStub, endpoint, payload):
        authStub.refresh_token()
        
        headers = {'content-type' : 'application/json'}
        r = requests.post(endpoint + '?access_token=' + authStub.authToken , data=json.dumps(payload), headers=headers)
        
        obj = super(ET_PostRest, self).__init__(r, True)
        return obj
    
########
##
##    Restful webservice to Get data
##
########
class ET_PatchRest(ET_Constructor):
    def __init__(self, authStub, endpoint, payload):
        authStub.refresh_token()
        
        headers = {'content-type' : 'application/json'}
        r = requests.patch(endpoint + '?access_token=' + authStub.authToken , data=json.dumps(payload), headers=headers)
        
        obj = super(ET_PatchRest, self).__init__(r, True)
        return obj

########
##
##    Restful webservice to Get data
##
########
class ET_DeleteRest(ET_Constructor):
    def __init__(self, authStub, endpoint):
        authStub.refresh_token()
        
        r = requests.delete(endpoint + '?access_token=' + authStub.authToken)
        
        obj = super(ET_DeleteRest, self).__init__(r, True)
        return obj
    
        '''
        qs = {"access_token" => authStub.authToken}
            
        uri = URI.parse(endpoint)
        uri.query = URI.encode_www_form(qs)
        http = Net::HTTP.new(uri.host, uri.port)
        http.use_ssl = true
        request = Net::HTTP::Delete.new(uri.request_uri)        
        requestResponse = http.request(request)
        super(requestResponse, true)
        '''

########
##
##    Get data
##
########
class ET_CUDSupport(ET_GetSupport):
    
    def __init__(self):
        super(ET_CUDSupport, self).__init__()
        
    def post(self):
        '''
        if props and props.is_a? Hash then
            @props = props
        end
        '''
        
        if self.extProps is not None:
            for k, v in self.extProps.iteritems():
                self.props[k.capitalize] = v
        
        obj = ET_Post(self.authStub, self.objType, self.props)
        return obj
    
    def patch(self):
        '''
        if props and props.is_a? Hash then
            @props = props
        end
        '''
        obj = ET_Patch(self.authStub, self.objType, self.props)
        return obj

    def delete(self):
        '''
        if props and props.is_a? Hash then
            @props = props
        '''
        obj = ET_Delete(self.authStub, self.objType, self.props)
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

        obj = ET_GetRest(self.authStub, completeURL, additionalQS)    
        
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

        obj = ET_PostRest(self.authStub, completeURL, self.props)
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
        
        obj = ET_PatchRest(self.authStub, completeURL, self.props)            
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

        obj = ET_DeleteRest(self.authStub, completeURL)
        return obj

########
##
##    wrap an Exact Target Content Area
##
########
class ET_ContentArea(ET_CUDSupport):    
    def __init__(self):
        super(ET_ContentArea, self).__init__()
        self.objType = 'ContentArea'

########
##
##    wrap an Exact Target Bounce Event
##
########
class ET_BounceEvent(ET_GetSupport):
    def __init__(self):
        self.objType = 'BounceEvent'
     
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
    
class ET_Campaign_Asset(ET_CUDSupportRest):
    def __init__(self):
        super(ET_Campaign_Asset, self).__init__()
        self.endpoint = 'https://www.exacttargetapis.com/hub/v1/campaigns/{id}/assets/{assetId}'
        self.urlProps = ["id", "assetId"]
        self.urlPropsRequired = ["id"]
        
########
##
##    wrap an Exact Target Bounce Event
##
########
class ET_ClickEvent(ET_GetSupport):
    def __init__(self):
        super(ET_ClickEvent, self).__init__()
        self.objType = 'ClickEvent'
        
########
##
##    wrap an Exact Target List and List Subscriber
##
########
class ET_List(ET_CUDSupport):
    def __init__(self):
        super(ET_List, self).__init__()
        self.objType = 'List'
    
class ET_List_Subscriber(ET_GetSupport):
    def __init__(self):
        super(ET_List_Subscriber, self).__init__()
        self.objType = 'ListSubscriber'