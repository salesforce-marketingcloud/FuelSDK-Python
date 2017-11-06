import ET_Client

try:
    debug = False
    stubObj = ET_Client.ET_Client(False, debug)
    
    # NOTE: These examples only work in accounts where the SubscriberKey functionality is not enabled
    #       SubscriberKey will need to be included in the props if that feature is enabled
    
    NewListName = "PythonSDKListSubscriber"
    SubscriberTestEmail = "PythonSDKListSubscriber@bh.exacttarget.com"
    
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
    
    
    # Make sure the list created correctly before 
    if postResponse.status: 
        
        newListID = postResponse.results[0]['NewID']
    
        # Create Subscriber On List 
        print('>>> Create Subscriber On List')
        postSub = ET_Client.ET_Subscriber()
        postSub.auth_stub = stubObj
        postSub.props = {"EmailAddress" : SubscriberTestEmail, "Lists" :[{"ID" : newListID}]}
        postResponse = postSub.post()
        print('Post Status: ' + str(postResponse.status))
        print('Code: ' + str(postResponse.code))
        print('Message: ' + str(postResponse.message))
        print('Result Count: ' + str(len(postResponse.results)))
        print('Results: ' + str(postResponse.results))
       
        if postResponse.status is False: 
            # If the subscriber already exists in the account then we need to do an update.
            # Update Subscriber On List 
            if postResponse.results[0]['ErrorCode'] == 12014:     
                # Update Subscriber to add to List
                print('>>> Update Subscriber to add to List')
                patchSub = ET_Client.ET_Subscriber()
                patchSub.auth_stub = stubObj
                patchSub.props = {"EmailAddress" : SubscriberTestEmail, "Lists" :[{"ID" : newListID}]}
                patchResponse = patchSub.patch()
                print('Patch Status: ' + str(patchResponse.status))
                print('Code: ' + str(patchResponse.code))
                print('Message: ' + str(patchResponse.message))
                print('Result Count: ' + str(len(patchResponse.results)))
                print('Results: ' + str(patchResponse.results))
        
        # Retrieve all Subscribers on the List
        print('>>> Retrieve all Subscribers on the List')
        getListSubs = ET_Client.ET_List_Subscriber()
        getListSubs.auth_stub = stubObj
        getListSubs.props = ["ObjectID","SubscriberKey","CreatedDate","Client.ID","Client.PartnerClientKey","ListID","Status"]
        getListSubs.search_filter = {'Property' : 'ListID','SimpleOperator' : 'equals','Value' : newListID}
        getResponse = getListSubs.get()
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

except Exception as e:
    print('Caught exception: ' + e.message)
    print(e)