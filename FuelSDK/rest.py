import requests
import json
import copy

    
########
##
##  Parent class used to determine what status we are in depending on web service call results
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
                if body and 'RequestID' in body:
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
        for k, v in list(props_dict.items()):
            if k in ws_object:
                ws_object[k] = v
            else:
                message = k + ' is not a property of ' + obj_type
                raise Exception(message)
        return ws_object

    def parse_props_into_ws_object(self, auth_stub, obj_type, props):
        empty_obj = auth_stub.soap_client.factory.create(obj_type)
        if props is not None and type(props) is dict:
            ws_create = copy.copy(empty_obj)
            ws_create = self.parse_props_dict_into_ws_object(obj_type, ws_create, props)
            return ws_create
        elif props is not None and type(props) is list:
            ws_create_list = []
            for prop_dict in props:
                #~ print str(datetime.now())+" - start"
                ws_create = copy.copy(empty_obj)
                ws_create = self.parse_props_dict_into_ws_object(obj_type, ws_create, prop_dict)
                #~ print str(datetime.now())+" - start"
                ws_create_list.append(ws_create)
            return ws_create_list
        else:
            message = 'Can not post properties to ' + obj_type + ' without a dict or list of properties'
            raise Exception(message)

########
##
##  Used to Describe Objects via web service call
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
##    Used to Configure Objects via web service call
##
########
class ET_Configure(ET_Constructor):
    def __init__(self, auth_stub, obj_type, props = None, update = False, delete = False):
        auth_stub.refresh_token()

        ws_configureRequest = auth_stub.soap_client.factory.create('ConfigureRequestMsg')
        action = 'create'
        if delete:
            action = 'delete'
        elif update:
            action = 'update'
        ws_configureRequest.Action = action
        ws_configureRequest.Configurations = {'Configuration': self.parse_props_into_ws_object(auth_stub, obj_type, props)}

        response = auth_stub.soap_client.service.Configure(None, ws_configureRequest)        

        if response is not None:
            #self.message = 'Describe: ' + obj_type
            super(ET_Configure, self).__init__(response)

########
##
##  Get call to a web service
##
########
class ET_Get(ET_Constructor):
    def __init__(self, auth_stub, obj_type, props = None, search_filter = None, options = None):        
        auth_stub.refresh_token()
        
        if props is None:   #if there are no properties to retrieve for the obj_type then return a Description of obj_type
            describe = ET_Describe(auth_stub, obj_type)
            props = []
            for prop in describe.results[0].Properties:
                if prop.IsRetrievable:
                    props.append(prop.Name) 

        ws_retrieveRequest = auth_stub.soap_client.factory.create('RetrieveRequest')
                
        if props is not None:
            if type(props) is dict: # If the properties is a hash, then we just want to use the keys
                ws_retrieveRequest.Properties = list(props.keys())
            else:
                ws_retrieveRequest.Properties = props

        if search_filter is not None:
            if 'LogicalOperator' in search_filter:
                ws_simpleFilterPartLeft = auth_stub.soap_client.factory.create('SimpleFilterPart')
                for prop in ws_simpleFilterPartLeft:
                    #print prop[0]
                    if prop[0] in search_filter['LeftOperand']:         
                        ws_simpleFilterPartLeft[prop[0]] = search_filter['LeftOperand'][prop[0]]    
                        
                ws_simpleFilterPartRight = auth_stub.soap_client.factory.create('SimpleFilterPart')
                for prop in ws_simpleFilterPartRight:
                    if prop[0] in search_filter['RightOperand']:
                        ws_simpleFilterPartRight[prop[0]] = search_filter['RightOperand'][prop[0]]
                        
                ws_complexFilterPart = auth_stub.soap_client.factory.create('ComplexFilterPart')
                ws_complexFilterPart.LeftOperand = ws_simpleFilterPartLeft
                ws_complexFilterPart.RightOperand = ws_simpleFilterPartRight
                ws_complexFilterPart.LogicalOperator = search_filter['LogicalOperator']
                for additional_operand in search_filter.get('AdditionalOperands', []):
                    ws_simpleFilterPart = auth_stub.soap_client.factory.create('SimpleFilterPart')
                    for k, v in list(additional_operand.items()):
                        ws_simpleFilterPart[k] = v
                    ws_complexFilterPart.AdditionalOperands.Operand.append(ws_simpleFilterPart)

                ws_retrieveRequest.Filter = ws_complexFilterPart
            else:
                ws_simpleFilterPart = auth_stub.soap_client.factory.create('SimpleFilterPart')
                for prop in ws_simpleFilterPart:
                    if prop[0] in search_filter:
                        ws_simpleFilterPart[prop[0]] = search_filter[prop[0]]
                ws_retrieveRequest.Filter = ws_simpleFilterPart

        if options is not None:
            for key, value in options.items():
                if isinstance(value, dict):
                    for k, v in value.items():
                        ws_retrieveRequest.Options[key][k] = v
                else:
                    ws_retrieveRequest.Options[key] = value

        ws_retrieveRequest.ObjectType = obj_type
        
        response = auth_stub.soap_client.service.Retrieve(ws_retrieveRequest)       

        if response is not None:
            super(ET_Get, self).__init__(response)

########
##
##  Call the Exact Target web service Create method
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
##  Call the Exact Target web service Update method
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
##  Call the Exact Target web service Delete method
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
##  Call the Exact Target web service RetrieveRequest passing in ContinueRequest param
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
##  set up variables for children objects to share
##
########
class ET_BaseObject(object):
    auth_stub = None
    obj = None
    last_request_id = None
    path = None
    props = None
    extProps = None
    search_filter = None
    options = None

########
##
##  make sure needed information is available and then make the call to ET_Get to call the webservice
##
########
class ET_GetSupport(ET_BaseObject):
    obj_type = 'ET_GetSupport'   #should be overwritten by inherited class
    
    def get(self, m_props = None, m_filter = None, m_options = None):
        props = self.props
        search_filter = self.search_filter
        options = self.options
        
        if m_props is not None and type(m_props) is list:
            props = m_props     
        elif self.props is not None and type(self.props) is dict:
            props = list(self.props.keys())

        if m_filter is not None and type(m_filter) is dict:
            search_filter = m_filter

        if m_options is not None and type(m_filter) is dict:
            options = m_options

        obj = ET_Get(self.auth_stub, self.obj_type, props, search_filter, options)
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
##  Restful webservice to Get data
##
########
class ET_GetRest(ET_Constructor):
    def __init__(self, auth_stub, endpoint, qs = None):
        auth_stub.refresh_token()   
        fullendpoint = endpoint
        urlSeparator = '?'
        for qStringValue in qs:
            fullendpoint += urlSeparator +    qStringValue + '=' + str(qs[qStringValue])
            urlSeparator = '&'

        headers = {'authorization' : 'Bearer ' + auth_stub.authToken,  'user-agent' : 'FuelSDK-Python-v1.3.0'}
        r = requests.get(fullendpoint, headers=headers)
    
        
        self.more_results = False
                    
        obj = super(ET_GetRest, self).__init__(r, True)
        return obj

########
##
##  Restful webservice to Get data
##
########
class ET_PostRest(ET_Constructor):  
    def __init__(self, auth_stub, endpoint, payload):
        auth_stub.refresh_token()
        
        headers = {'content-type' : 'application/json', 'user-agent' : 'FuelSDK-Python-v1.3.0', 'authorization' : 'Bearer ' + auth_stub.authToken}
        r = requests.post(endpoint, data=json.dumps(payload), headers=headers)
        
        obj = super(ET_PostRest, self).__init__(r, True)
        return obj
    
########
##
##  Restful webservice to Get data
##
########
class ET_PatchRest(ET_Constructor):
    def __init__(self, auth_stub, endpoint, payload):
        auth_stub.refresh_token()
        
        headers = {'content-type' : 'application/json', 'user-agent' : 'FuelSDK-Python-v1.3.0', 'authorization' : 'Bearer ' + auth_stub.authToken}
        r = requests.patch(endpoint , data=json.dumps(payload), headers=headers)
        
        obj = super(ET_PatchRest, self).__init__(r, True)
        return obj

########
##
##  Restful webservice to Get data
##
########
class ET_DeleteRest(ET_Constructor):
    def __init__(self, auth_stub, endpoint):
        auth_stub.refresh_token()

        headers = {'authorization' : 'Bearer ' + auth_stub.authToken, 'user-agent' : 'FuelSDK-Python-v1.3.0'}
        r = requests.delete(endpoint, headers=headers)
        
        obj = super(ET_DeleteRest, self).__init__(r, True)
        return obj

########
##
##  Get data
##
########
class ET_CUDSupport(ET_GetSupport):
    
    def __init__(self):
        super(ET_CUDSupport, self).__init__()
        
    def post(self):
        if self.extProps is not None:
            for k, v in self.extProps.items():
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
##  Get data using a REST call
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

        completeURL = self.auth_stub.base_api_url + self.path
        additionalQS = {}
        
        if self.props is not None and type(self.props) is dict:
            for k, v in self.props.items():
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
        if 'page' in obj.results: 
            self.lastPageNumber = obj.results['page']
            pageSize = obj.results['pageSize']
            if 'count' in obj.results: 
                count = obj.results['count']
            elif 'totalCount' in obj.results: 
                count = obj.results['totalCount']
                    
            if count is not None and count > (self.lastPageNumber * pageSize):
                obj.more_results = True
            else:
                obj.more_results = False            
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
        
        obj = self.get()
        
        if removePageFromProps:
            del self.props['$page']
        else:
            self.props['$page'] = originalPageValue
        
        return obj

########
##
##  Create, Update and Delete using a REST call
##
########            
class ET_CUDSupportRest(ET_GetSupportRest):
    path = None
    urlProps = None
    urlPropsRequired = None
    
    def __init__(self):
        super
    
    def post(self):
        completeURL = self.auth_stub.base_api_url + self.path
        
        if self.props is not None and type(self.props) is dict:
            for k, v in self.props.items():
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
        completeURL = self.auth_stub.base_api_url + self.path
        # All URL Props are required when doing Patch   
        for value in self.urlProps: 
            if self.props is None or value not in self.props:
                raise "Unable to process request due to missing required prop: #{value}"
        
        if self.props is not None and type(self.props) is dict:
            for k, v in self.props.items():
                if k in self.urlProps:
                    completeURL = completeURL.replace('{{{0}}}'.format(k), v)
        
        obj = ET_PatchRest(self.auth_stub, completeURL, self.props)         
        return obj
    
    def delete(self):
        completeURL = self.auth_stub.base_api_url + self.path
        # All URL Props are required when doing Patch   
        for value in self.urlProps: 
            if self.props is None or value not in self.props:
                raise "Unable to process request due to missing required prop: #{value}"
        
        if self.props is not None and type(self.props) is dict:     
            for k, v in self.props.items():
                if k in self.urlProps:
                    completeURL = completeURL.replace('{{{0}}}'.format(k), v)

        obj = ET_DeleteRest(self.auth_stub, completeURL)
        return obj
