from .ET_Client.py import ET_Client

try:
    debug = False
    stubObj = ET_Client.ET_Client(False, debug)
  
    # Retrieve All Folder with GetMoreResults
    print '>>> Retrieve All Folder with GetMoreResults'
    getFolder = ET_Client.ET_Folder()
    getFolder.auth_stub = stubObj 
    getFolder.props = ["ID", "Client.ID", "ParentFolder.ID", "ParentFolder.CustomerKey", "ParentFolder.ObjectID", "ParentFolder.Name", "ParentFolder.Description", "ParentFolder.ContentType", "ParentFolder.IsActive", "ParentFolder.IsEditable", "ParentFolder.AllowChildren", "Name", "Description", "ContentType", "IsActive", "IsEditable", "AllowChildren", "CreatedDate", "ModifiedDate", "Client.ModifiedBy", "ObjectID", "CustomerKey", "Client.EnterpriseID", "Client.CreatedBy"]  
    getResponse = getFolder.get()
    print 'Retrieve Status: ' + str(getResponse.status)
    print 'Code: ' + str(getResponse.code)
    print 'Message: ' + str(getResponse.message)
    print 'MoreResults: ' + str(getResponse.more_results)
    print 'Results Length: ' + str(len(getResponse.results))
    #print 'Results: ' + str(getResponse.results)

    while getResponse.more_results: 
        print '>>> Continue Retrieve All Folder with GetMoreResults'
        getResponse = getFolder.getMoreResults()
        print 'Retrieve Status: ' + str(getResponse.status)
        print 'Code: ' + str(getResponse.code)
        print 'Message: ' + str(getResponse.message)
        print 'MoreResults: ' + str(getResponse.more_results)
        print 'RequestID: ' + str(getResponse.request_id)
        print 'Results Length: ' + str(len(getResponse.results))

    NameOfTestFolder = "PythonSDKFolder"
    
    # Retrieve Specific Folder for Email Folder ParentID
    print '>>> Retrieve Specific Folder for Email Folder ParentID'
    getFolder = ET_Client.ET_Folder()
    getFolder.auth_stub = stubObj 
    getFolder.props = ["ID"]  
    #getFolder.search_filter =  {'Property' : 'ContentType','SimpleOperator' : 'equals','Value' : "email"}
    getFolder.search_filter =  {'LeftOperand' : {'Property' : 'ContentType','SimpleOperator' : 'equals','Value' : "email"}, 'RightOperand' : {'Property' : 'ParentFolder.ID','SimpleOperator' : 'equals','Value' : "0"}, 'LogicalOperator' : 'AND'}
    getResponse = getFolder.get()
    print 'Retrieve Status: ' + str(getResponse.status)
    print 'Code: ' + str(getResponse.code)
    print 'Message: ' + str(getResponse.message)
    print 'MoreResults: ' + str(getResponse.more_results)
    print 'Results Length: ' + str(len(getResponse.results))
    print 'Results: ' + str(getResponse.results)
    
    ParentIDForEmail = getResponse.results[0].ID
    print 'Parent Folder for Email: ' + str(ParentIDForEmail)

    # Create Folder 
    print '>>> Create Folder'
    postFolder = ET_Client.ET_Folder()
    postFolder.auth_stub = stubObj
    postFolder.props = {"CustomerKey" :  NameOfTestFolder, "Name" :  NameOfTestFolder, "Description" :  NameOfTestFolder, "ContentType":  "EMAIL", "ParentFolder" :  {"ID" :  ParentIDForEmail}}   
    postResponse = postFolder.post()
    print 'Post Status: ' + str(postResponse.status)
    print 'Code: ' + str(postResponse.code)
    print 'Message: ' + str(postResponse.message)
    print 'Result Count: ' + str(len(postResponse.results))
    print 'Results: ' + str(postResponse.results)    
  
    # Retrieve newly created Folder
    print '>>> Retrieve newly created Folder'
    getFolder = ET_Client.ET_Folder()
    getFolder.auth_stub = stubObj 
    getFolder.props = ["ID", "Client.ID", "ParentFolder.ID", "ParentFolder.CustomerKey", "ParentFolder.ObjectID", "ParentFolder.Name", "ParentFolder.Description", "ParentFolder.ContentType", "ParentFolder.IsActive", "ParentFolder.IsEditable", "ParentFolder.AllowChildren", "Name", "Description", "ContentType", "IsActive", "IsEditable", "AllowChildren", "CreatedDate", "ModifiedDate", "Client.ModifiedBy", "ObjectID", "CustomerKey", "Client.EnterpriseID", "Client.CreatedBy"]  
    getFolder.search_filter =  {'Property' : 'CustomerKey','SimpleOperator' : 'equals','Value' : NameOfTestFolder}
    getResponse = getFolder.get()
    print 'Retrieve Status: ' + str(getResponse.status)
    print 'Code: ' + str(getResponse.code)
    print 'Message: ' + str(getResponse.message)
    print 'MoreResults: ' + str(getResponse.more_results)    
    print 'Results Length: ' + str(len(getResponse.results))
    print 'Results: ' + str(getResponse.results)
    
    # Update Folder 
    print '>>> Update Folder'
    patchFolder = ET_Client.ET_Folder()
    patchFolder.auth_stub = stubObj
    patchFolder.props = {"CustomerKey" :  NameOfTestFolder, "Name" :  NameOfTestFolder, "Description" :  "Updated Description"}    
    patchResponse = patchFolder.patch()
    print 'Patch Status: ' + str(patchResponse.status)
    print 'Code: ' + str(patchResponse.code)
    print 'Message: ' + str(patchResponse.message)
    print 'Result Count: ' + str(len(patchResponse.results))
    print 'Results: ' + str(patchResponse.results)
    
    # Retrieve updated Folder
    print '>>> Retrieve updated Folder'
    getFolder = ET_Client.ET_Folder()
    getFolder.auth_stub = stubObj 
    getFolder.props = ["ID", "Client.ID", "ParentFolder.ID", "ParentFolder.CustomerKey", "ParentFolder.ObjectID", "ParentFolder.Name", "ParentFolder.Description", "ParentFolder.ContentType", "ParentFolder.IsActive", "ParentFolder.IsEditable", "ParentFolder.AllowChildren", "Name", "Description", "ContentType", "IsActive", "IsEditable", "AllowChildren", "CreatedDate", "ModifiedDate", "Client.ModifiedBy", "ObjectID", "CustomerKey", "Client.EnterpriseID", "Client.CreatedBy"]  
    getFolder.search_filter =  {'Property' : 'CustomerKey','SimpleOperator' : 'equals','Value' : NameOfTestFolder}
    getResponse = getFolder.get()
    print 'Retrieve Status: ' + str(getResponse.status)
    print 'Code: ' + str(getResponse.code)
    print 'Message: ' + str(getResponse.message)
    print 'MoreResults: ' + str(getResponse.more_results)    
    print 'Results Length: ' + str(len(getResponse.results))
    print 'Results: ' + str(getResponse.results)
        
    # Delete Folder 
    print '>>> Delete Folder'
    deleteFolder = ET_Client.ET_Folder()
    deleteFolder.auth_stub = stubObj
    deleteFolder.props = {"CustomerKey" : NameOfTestFolder}   
    deleteResponse = deleteFolder.delete()
    print 'Delete Status: ' + str(deleteResponse.status)
    print 'Code: ' + str(deleteResponse.code)
    print 'Message: ' + str(deleteResponse.message)
    print 'Result Count: ' + str(len(deleteResponse.results))
    print 'Results: ' + str(deleteResponse.results)
        
    # Retrieve Folder to confirm deletion
    print '>>> Retrieve Folder to confirm deletion'
    getFolder = ET_Client.ET_Folder()
    getFolder.auth_stub = stubObj 
    getFolder.props = ["ID"]  
    getFolder.search_filter =  {'Property' : 'CustomerKey','SimpleOperator' : 'equals','Value' : NameOfTestFolder}
    getResponse = getFolder.get()
    print 'Retrieve Status: ' + str(getResponse.status)
    print 'Code: ' + str(getResponse.code)
    print 'Message: ' + str(getResponse.message)
    print 'MoreResults: ' + str(getResponse.more_results)    
    print 'Results Length: ' + str(len(getResponse.results))
    print 'Results: ' + str(getResponse.results)

except Exception as e:
    print 'Caught exception: ' + str(e.message)
    print e