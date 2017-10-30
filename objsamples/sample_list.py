import ET_Client

try:
    debug = False   
    stubObj = ET_Client.ET_Client(False, debug) 
    
    NewListName = "PythonSDKList"

    # Create List 
    print('>>> Create List')
    postList = ET_Client.ET_List()
    postList.auth_stub = stubObj
    postList.props = {"ListName" : NewListName, "Description" : "This list was created with the PythonSDK", "Type" : "Private" }        
    postResponse = postList.post()
    print('Post Status: ' + str(postResponse.status))
    print('Code: ' + str(postResponse.code))
    print('Message: ' + str(postResponse.message))
    print('Result Count: ' + str(len(postResponse.results)))
    print('Results: ' + str(postResponse.results))
    
    
    # Make sure the list created correctly and the 1st dict in it has a NewID...
    if postResponse.status and 'NewID' in postResponse.results[0]:
        
        newListID = postResponse.results[0]['NewID']
    
        # Retrieve newly created List by ID
        print('>>> Retrieve newly created List')
        getList = ET_Client.ET_List()
        getList.auth_stub = stubObj
        getList.props = ["ID","PartnerKey","CreatedDate","ModifiedDate","Client.ID","Client.PartnerClientKey","ListName","Description","Category","Type","CustomerKey","ListClassification","AutomatedEmail.ID"]
        getList.search_filter =  {'Property' : 'ID','SimpleOperator' : 'equals','Value' : newListID}
        getResponse = getList.get()
        print('Retrieve Status: ' + str(getResponse.status))
        print('Code: ' + str(getResponse.code))
        print('Message: ' + str(getResponse.message))
        print('MoreResults: ' + str(getResponse.more_results))   
        print('Results Length: ' + str(len(getResponse.results)))
        print('Results: ' + str(getResponse.results))            
            
        # Update List 
        print('>>> Update List')
        patchSub = ET_Client.ET_List()
        patchSub.auth_stub = stubObj
        patchSub.props = {"ID" : newListID, "Description" : "I updated the description"}        
        patchResponse = patchSub.patch()
        print('Patch Status: ' + str(patchResponse.status))
        print('Code: ' + str(patchResponse.code))
        print('Message: ' + str(patchResponse.message))
        print('Result Count: ' + str(len(patchResponse.results)))
        print('Results: ' + str(patchResponse.results))
        
        # Retrieve List that should have description updated 
        print('>>> Retrieve List that should have description updated ')
        getList = ET_Client.ET_List()
        getList.auth_stub = stubObj 
        getList.props = ["ID","PartnerKey","CreatedDate","ModifiedDate","Client.ID","Client.PartnerClientKey","ListName","Description","Category","Type","CustomerKey","ListClassification","AutomatedEmail.ID"]
        getList.search_filter =  {'Property' : 'ID','SimpleOperator' : 'equals','Value' : newListID}
        getResponse = getList.get()
        print('Retrieve Status: ' + str(getResponse.status))
        print('Code: ' + str(getResponse.code))
        print('Message: ' + str(getResponse.message))
        print('MoreResults: ' + str(getResponse.more_results))   
        print('Results Length: ' + str(len(getResponse.results)))
        print('Results: ' + str(getResponse.results))
        
        # Delete List
        print('>>> Delete List')
        deleteSub = ET_Client.ET_List()
        deleteSub.auth_stub = stubObj   
        deleteSub.props = {"ID" : newListID}
        deleteResponse = deleteSub.delete()
        print('Delete Status: ' + str(deleteResponse.status))
        print('Code: ' + str(deleteResponse.code))
        print('Message: ' + str(deleteResponse.message)) 
        print('Results Length: ' + str(len(deleteResponse.results)))
        print('Results: ' + str(deleteResponse.results))
        
        # Retrieve List to confirm deletion
        print('>>> Retrieve List to confirm deletion')
        getList = ET_Client.ET_List()
        getList.auth_stub = stubObj 
        getList.props = ["ID","PartnerKey","CreatedDate","ModifiedDate","Client.ID","Client.PartnerClientKey","ListName","Description","Category","Type","CustomerKey","ListClassification","AutomatedEmail.ID"]
        getList.search_filter =  {'Property' : 'ID','SimpleOperator' : 'equals','Value' : newListID}
        getResponse = getList.get()
        print('Retrieve Status: ' + str(getResponse.status))
        print('Code: ' + str(getResponse.code))
        print('Message: ' + str(getResponse.message))
        print('MoreResults: ' + str(getResponse.more_results))   
        print('Results Length: ' + str(len(getResponse.results)))
        print('Results: ' + str(getResponse.results))

except Exception as e:
    print('Caught exception: ' + str(e.message))


