import ET_Client

try:
    debug = False
    stubObj = ET_Client.ET_Client(False, debug)
  
    # Retrieve All ContentArea with GetMoreResults
    print('>>> Retrieve All ContentArea with GetMoreResults')
    getContent = ET_Client.ET_ContentArea()
    getContent.auth_stub = stubObj 
    getContent.props = ["RowObjectID","ObjectID","ID","CustomerKey","Client.ID","ModifiedDate","CreatedDate","CategoryID","Name","Layout","IsDynamicContent","Content","IsSurvey","IsBlank","Key"]  
    getResponse = getContent.get()
    print('Retrieve Status: ' + str(getResponse.status))
    print('Code: ' + str(getResponse.code))
    print('Message: ' + str(getResponse.message))
    print('MoreResults: ' + str(getResponse.more_results))
    print('Results Length: ' + str(len(getResponse.results)))
    #print 'Results: ' + str(getResponse.results)

    while getResponse.more_results: 
        print('>>> Continue Retrieve All ContentArea with GetMoreResults')
        getResponse = getContent.getMoreResults()
        print('Retrieve Status: ' + str(getResponse.status))
        print('Code: ' + str(getResponse.code))
        print('Message: ' + str(getResponse.message))
        print('MoreResults: ' + str(getResponse.more_results))
        print('RequestID: ' + str(getResponse.request_id))
        print('Results Length: ' + str(len(getResponse.results)))

    NameOfTestContentArea = "PythonSDKContentArea"

    # Create ContentArea 
    print('>>> Create ContentArea')
    postContent = ET_Client.ET_ContentArea()
    postContent.auth_stub = stubObj
    postContent.props = {"CustomerKey" : NameOfTestContentArea, "Name" : NameOfTestContentArea, "Content": "<b>Some HTML Content Goes here</b>"}   
    postResponse = postContent.post()
    print('Post Status: ' + str(postResponse.status))
    print('Code: ' + str(postResponse.code))
    print('Message: ' + str(postResponse.message))
    print('Result Count: ' + str(len(postResponse.results)))
    print('Results: ' + str(postResponse.results))    
  
    # Retrieve newly created ContentArea
    print('>>> Retrieve newly created ContentArea')
    getContent = ET_Client.ET_ContentArea()
    getContent.auth_stub = stubObj 
    getContent.props = ["RowObjectID","ObjectID","ID","CustomerKey","Client.ID","ModifiedDate","CreatedDate","CategoryID","Name","Layout","IsDynamicContent","Content","IsSurvey","IsBlank","Key"]  
    getContent.search_filter =  {'Property' : 'CustomerKey','SimpleOperator' : 'equals','Value' : NameOfTestContentArea}
    getResponse = getContent.get()
    print('Retrieve Status: ' + str(getResponse.status))
    print('Code: ' + str(getResponse.code))
    print('Message: ' + str(getResponse.message))
    print('MoreResults: ' + str(getResponse.more_results))    
    print('Results Length: ' + str(len(getResponse.results)))
    print('Results: ' + str(getResponse.results))
    
    # Update ContentArea 
    print('>>> Update ContentArea')
    patchContent = ET_Client.ET_ContentArea()
    patchContent.auth_stub = stubObj
    patchContent.props = {"CustomerKey" : NameOfTestContentArea, "Name":NameOfTestContentArea, "Content": "<b>Some HTML Content Goes here. NOW WITH NEW CONTENT</b>"}    
    patchResponse = patchContent.patch()
    print('Patch Status: ' + str(patchResponse.status))
    print('Code: ' + str(patchResponse.code))
    print('Message: ' + str(patchResponse.message))
    print('Result Count: ' + str(len(patchResponse.results)))
    print('Results: ' + str(patchResponse.results))
    
    # Retrieve updated ContentArea
    print('>>> Retrieve updated ContentArea')
    getContent = ET_Client.ET_ContentArea()
    getContent.auth_stub = stubObj 
    getContent.props = ["RowObjectID","ObjectID","ID","CustomerKey","Client.ID","ModifiedDate","CreatedDate","CategoryID","Name","Layout","IsDynamicContent","Content","IsSurvey","IsBlank","Key"]  
    getContent.search_filter =  {'Property' : 'CustomerKey','SimpleOperator' : 'equals','Value' : NameOfTestContentArea}
    getResponse = getContent.get()
    print('Retrieve Status: ' + str(getResponse.status))
    print('Code: ' + str(getResponse.code))
    print('Message: ' + str(getResponse.message))
    print('MoreResults: ' + str(getResponse.more_results))    
    print('Results Length: ' + str(len(getResponse.results)))
    print('Results: ' + str(getResponse.results))
        
    # Delete ContentArea 
    print('>>> Delete ContentArea')
    deleteContent = ET_Client.ET_ContentArea()
    deleteContent.auth_stub = stubObj
    deleteContent.props = {"CustomerKey" : NameOfTestContentArea, "Name":NameOfTestContentArea, "Content": "<b>Some HTML Content Goes here. NOW WITH NEW CONTENT</b>"}   
    deleteResponse = deleteContent.delete()
    print('Delete Status: ' + str(deleteResponse.status))
    print('Code: ' + str(deleteResponse.code))
    print('Message: ' + str(deleteResponse.message))
    print('Result Count: ' + str(len(deleteResponse.results)))
    print('Results: ' + str(deleteResponse.results))
        
    # Retrieve ContentArea to confirm deletion
    print('>>> Retrieve ContentArea to confirm deletion')
    getContent = ET_Client.ET_ContentArea()
    getContent.auth_stub = stubObj 
    getContent.props = ["RowObjectID","ObjectID","ID","CustomerKey","Client.ID","ModifiedDate","CreatedDate","CategoryID","Name","Layout","IsDynamicContent","Content","IsSurvey","IsBlank","Key"]  
    getContent.search_filter =  {'Property' : 'CustomerKey','SimpleOperator' : 'equals','Value' : NameOfTestContentArea}
    getResponse = getContent.get()
    print('Retrieve Status: ' + str(getResponse.status))
    print('Code: ' + str(getResponse.code))
    print('Message: ' + str(getResponse.message))
    print('MoreResults: ' + str(getResponse.more_results))    
    print('Results Length: ' + str(len(getResponse.results)))
    print('Results: ' + str(getResponse.results))

except Exception as e:
    print('Caught exception: ' + str(e.message))
    print(e)