from FuelSDK.rest import ET_CUDSupport,ET_CUDSupportRest,ET_GetSupport,ET_Get,ET_Patch,ET_Post,ET_Delete,ET_Configure,ET_Describe

########
##
##  wrap an Exact Target Content Area
##
########
class ET_ContentArea(ET_CUDSupport):    
    def __init__(self):
        super(ET_ContentArea, self).__init__()
        self.obj_type = 'ContentArea'

########
##
##  wrap an Exact Target DataFolder
##
########
class ET_Folder(ET_CUDSupport): 
    def __init__(self):
        super(ET_Folder, self).__init__()
        self.obj_type = 'DataFolder'

########
##
##    wrap an Exact Target PropertyDefinition
##
########
class ET_ProfileAttribute():    
    def __init__(self):
        self.obj_type = 'PropertyDefinition'
        self.update = False
        self.delete = False

    def post(self):       
        obj = ET_Configure(self.auth_stub, self.obj_type, self.props, self.update, self.delete)
        if obj is not None:
            self.last_request_id = obj.request_id
        return obj

    def get(self):
        return ET_Describe(self.auth_stub, 'Subscriber')

########
##
##  wrap an Exact Target Bounce Event
##
########
class ET_BounceEvent(ET_GetSupport):
    def __init__(self):
        self.obj_type = 'BounceEvent'
     
########
##
##  wrap an Exact Target Campaign and associated Assets
##
########        
class ET_Campaign(ET_CUDSupportRest):
    def __init__(self):
        super(ET_Campaign, self).__init__()
        self.path = '/hub/v1/campaigns/{id}'
        self.urlProps = ["id"]
        self.urlPropsRequired = []
        
    ##the patch rest service is not implemented for campaigns yet.  use post instead and remove this when patch is implemented on the back end
    def patch(self):
        self.path = '/hub/v1/campaigns'  #don't put the id on the url when patching via post
        obj = super(ET_Campaign, self).post()
        self.path = '/hub/v1/campaigns/{id}' #but set it back to the url with id for other operations to continue working
        return obj
    
class ET_Campaign_Asset(ET_CUDSupportRest):
    def __init__(self):
        super(ET_Campaign_Asset, self).__init__()
        self.path = '/hub/v1/campaigns/{id}/assets/{assetId}'
        self.urlProps = ["id", "assetId"]
        self.urlPropsRequired = ["id"]
        
########
##
##  wrap an Exact Target Click Event
##
########
class ET_ClickEvent(ET_GetSupport):
    def __init__(self):
        super(ET_ClickEvent, self).__init__()
        self.obj_type = 'ClickEvent'
        
########
##
##  wrap an Exact Target List and List Subscriber
##
########
class ET_Group(ET_CUDSupport):
    def __init__(self):
        super(ET_Group, self).__init__()
        self.obj_type = 'Group'

class ET_Send(ET_CUDSupport):
    def __init__(self):
        super(ET_Send, self).__init__()
        self.obj_type = 'Send'

class ET_ListSend(ET_CUDSupport):
    def __init__(self):
        super(ET_ListSend, self).__init__()
        self.obj_type = 'ListSend'

class ET_List(ET_CUDSupport):
    def __init__(self):
        super(ET_List, self).__init__()
        self.obj_type = 'List'

class ET_List_Subscriber(ET_GetSupport):
    def __init__(self):
        super(ET_List_Subscriber, self).__init__()
        self.obj_type = 'ListSubscriber'

class ET_SubscriberList(ET_GetSupport):
    def __init__(self):
        super(ET_SubscriberList, self).__init__()
        self.obj_type = 'SubscriberList'

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
    attributes  = None
    def __init__(self):
        super(ET_TriggeredSend, self).__init__()
        self.obj_type = 'TriggeredSendDefinition'

    def send(self):
        tscall = {"TriggeredSendDefinition":self.props, "Subscribers" : self.subscribers, "Attributes": self.attributes }
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
        
        if type(self.props) is list:
            currentPropList = []
            for rec in self.props:
                currentFields = []
                currentProp = {}
                
                for key, value in rec.items():
                    currentFields.append({"Name" : key, "Value" : value})
                
                currentProp['CustomerKey'] = self.CustomerKey
                currentProp['Properties'] = {}
                currentProp['Properties']['Property'] = currentFields
                
                currentPropList.append(currentProp)
            
            currentProp = currentPropList

        else:
            currentFields = []
            currentProp = {}
                
            for key, value in self.props.items():
                currentFields.append({"Name" : key, "Value" : value})

            currentProp['CustomerKey'] = self.CustomerKey
            currentProp['Properties'] = {}
            currentProp['Properties']['Property'] = currentFields   

        obj = ET_Post(self.auth_stub, self.obj_type, currentProp)   
        self.props = originalProps
        return obj
        
    def patch(self): 
        self.getCustomerKey()

        if type(self.props) is list:
            currentPropList = []
            for rec in self.props:
                currentFields = []
                currentProp = {}
                
                for key, value in rec.items():
                    currentFields.append({"Name" : key, "Value" : value})
                
                currentProp['CustomerKey'] = self.CustomerKey
                currentProp['Properties'] = {}
                currentProp['Properties']['Property'] = currentFields
                
                currentPropList.append(currentProp)
            
            currentProp = currentPropList
        else:
            currentFields = []
            currentProp = {}
            
            for key, value in self.props.items():
                currentFields.append({"Name" : key, "Value" : value})
            
            currentProp['CustomerKey'] = self.CustomerKey
            currentProp['Properties'] = {}
            currentProp['Properties']['Property'] = currentFields
            
        obj = ET_Patch(self.auth_stub, self.obj_type, currentProp)
        return obj
    
    def delete(self): 
        self.getCustomerKey()

        if type(self.props) is list:
            currentPropList = []
            for rec in self.props:
                currentFields = []
                currentProp = {}
                
                for key, value in rec.items():
                    currentFields.append({"Name" : key, "Value" : value})
                
                currentProp['CustomerKey'] = self.CustomerKey
                currentProp['Keys'] = {}
                currentProp['Keys']['Key'] = currentFields
                
                currentPropList.append(currentProp)
            
            currentProp = currentPropList
        else:
            currentFields = []
            currentProp = {}
                
            for key, value in self.props.items():
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
