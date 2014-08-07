import ET_Client

try:
    debug = False
    stubObj = ET_Client.ET_Client(False, debug)
    
    NewListName = "PythonSDKList"

    ## Example using AddSubscriberToList() method
    ## Typically this method will be used with a pre-existing list but for testing purposes one is being created.
    
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
    
    if postResponse.status: 
        
        newListID = postResponse.results[0]['NewID']
        # Adding Subscriber To a List
        print('>>> Add Subscriber To a List')
        AddSubResponse = stubObj.AddSubscriberToList("AddSubTesting@bh.exacttarget.com", [newListID])
        print('AddSubResponse Status: ' + str(AddSubResponse.status))
        print('Code: ' + str(AddSubResponse.code))
        print('Message: ' + str(AddSubResponse.message))
        print('Result Count: ' + str(len(AddSubResponse.results)))
        print('Results: ' + str(AddSubResponse.results))
                
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

except Exception as e:
    print('Caught exception: ' + e.message)
    print(e)