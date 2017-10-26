import ET_Client

try:
    debug = False
    stubObj = ET_Client.ET_Client(False, debug)
    
    # NOTE: These examples only work in accounts where the SubscriberKey functionality is not enabled
    #       SubscriberKey will need to be included in the props if that feature is enabled
    
    SubscriberTestEmail = "PythonSDKExample@bh.exacttarget.com"

    # Create Subscriber 
    print('>>> Create Subscriber')
    postSub = ET_Client.ET_Subscriber()
    postSub.auth_stub = stubObj
    postSub.props = {"EmailAddress" : SubscriberTestEmail}
    postResponse = postSub.post()
    print('Post Status: ' + str(postResponse.status))
    print('Code: ' + str(postResponse.code))
    print('Message: ' + str(postResponse.message))
    print('Result Count: ' + str(len(postResponse.results)))
    print('Results: ' + str(postResponse.results))
    
    # Retrieve newly created Subscriber
    print('>>> Retrieve newly created Subscriber')
    getSub = ET_Client.ET_Subscriber()
    getSub.auth_stub = stubObj
    getSub.props = ["SubscriberKey", "EmailAddress", "Status"]
    getSub.search_filter = {'Property' : 'SubscriberKey','SimpleOperator' : 'equals','Value' : SubscriberTestEmail}
    getResponse = getSub.get()
    print('Retrieve Status: ' + str(getResponse.status))
    print('Code: ' + str(getResponse.code))
    print('Message: ' + str(getResponse.message))
    print('MoreResults: ' + str(getResponse.more_results))
    print('Results Length: ' + str(len(getResponse.results)))
    print('Results: ' + str(getResponse.results))
        
    # Update Subscriber 
    print('>>> Update Subscriber')
    patchSub = ET_Client.ET_Subscriber()
    patchSub.auth_stub = stubObj
    patchSub.props = {"EmailAddress" : SubscriberTestEmail, "Status" : "Unsubscribed"}
    patchResponse = patchSub.patch()
    print('Patch Status: ' + str(patchResponse.status))
    print('Code: ' + str(patchResponse.code))
    print('Message: ' + str(patchResponse.message))
    print('Result Count: ' + str(len(patchResponse.results)))
    print('Results: ' + str(patchResponse.results))
    
    # Retrieve Subscriber that should have status unsubscribed now
    print('>>> Retrieve Subscriber that should have status unsubscribed now')
    getSub = ET_Client.ET_Subscriber()
    getSub.auth_stub = stubObj
    getSub.props = ["SubscriberKey", "EmailAddress", "Status"]
    getSub.search_filter = {'Property' : 'SubscriberKey','SimpleOperator' : 'equals','Value' : SubscriberTestEmail};
    getResponse = getSub.get()
    print('Retrieve Status: ' + str(getResponse.status))
    print('Code: ' + str(getResponse.code))
    print('Message: ' + str(getResponse.message))
    print('MoreResults: ' + str(getResponse.more_results))
    print('Results Length: ' + str(len(getResponse.results)))
    print('Results: ' + str(getResponse.results))
    
    # Delete Subscriber
    print('>>> Delete Subscriber')
    deleteSub = ET_Client.ET_Subscriber()
    deleteSub.auth_stub = stubObj
    deleteSub.props = {"EmailAddress" : SubscriberTestEmail}
    deleteResponse = deleteSub.delete()
    print('Delete Status: ' + str(deleteResponse.status))
    print('Code: ' + str(deleteResponse.code))
    print('Message: ' + str(deleteResponse.message))
    print('Results Length: ' + str(len(deleteResponse.results)))
    print('Results: ' + str(deleteResponse.results))
    
    # Retrieve Subscriber to confirm deletion
    print('>>> Retrieve Subscriber to confirm deletion')
    getSub = ET_Client.ET_Subscriber()
    getSub.auth_stub = stubObj
    getSub.props = ["SubscriberKey", "EmailAddress", "Status"]
    getSub.search_filter = {'Property' : 'SubscriberKey','SimpleOperator' : 'equals','Value' : SubscriberTestEmail};
    getResponse = getSub.get()
    print('Retrieve Status: ' + str(getResponse.status))
    print('Code: ' + str(getResponse.code))
    print('Message: ' + str(getResponse.message))
    print('MoreResults: ' + str(getResponse.more_results))
    print('Results Length: ' + str(len(getResponse.results)))
    print('Results: ' + str(getResponse.results))
        

    '''
    # Do not run the "Retrieve All Subscribers" request for testing if you have more than 100,000 records in your account as it will take a long time to complete.

    # Retrieve All Subcribers with GetMoreResults
    print '>>> Retrieve All Subcribers with GetMoreResults'
    getSub = ET_Client.ET_Subscriber()
    getSub.auth_stub = stubObj
    getSub.props = ["SubscriberKey", "EmailAddress", "Status"]
    getResponse = getSub.get()
    print 'Retrieve Status: ' + str(getResponse.status)
    print 'Code: ' + str(getResponse.code)
    print 'Message: ' + str(getResponse.message)
    print 'MoreResults: ' + str(getResponse.more_results)
    print 'RequestID: ' + str(getResponse.request_id)
    print 'Results Length: ' + str(len(getResponse.results))
    #print 'Results: ' + str(getResponse.results)

    while getResponse.more_results: 
        print '>>> Continue Retrieve All Subcribers with GetMoreResults'
        getResponse = getSub.getMoreResults()
        print 'Retrieve Status: ' + str(getResponse.status)
        print 'Code: ' + str(getResponse.code)
        print 'Message: ' + str(getResponse.message)
        print 'MoreResults: ' + str(getResponse.more_results)
        print 'RequestID: ' + str(getResponse.request_id)
        print 'Results Length: ' + str(len(getResponse.results))
    '''

except Exception as e:
    print('Caught exception: ' + str(e.message))
    print(e.backtrace)
