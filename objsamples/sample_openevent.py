import ET_Client

try:
    debug = False
    stubObj = ET_Client.ET_Client(False, debug)
        
    ## Modify the date below to reduce the number of results returned from the request
    ## Setting this too far in the past could result in a very large response size
    retrieveDate = '2013-01-15T13:00:00.000'

    print('>>> Retrieve Filtered OpenEvents with GetMoreResults')
    getOpenEvent = ET_Client.ET_OpenEvent()
    getOpenEvent.auth_stub = stubObj
    getOpenEvent.props = ["SendID","SubscriberKey","EventDate","Client.ID","EventType","BatchID","TriggeredSendDefinitionObjectID","PartnerKey"]
    getOpenEvent.search_filter = {'Property' : 'EventDate','SimpleOperator' : 'greaterThan','DateValue' : retrieveDate}
    getResponse = getOpenEvent.get()
    print('Retrieve Status: ' + str(getResponse.status))
    print('Code: ' + str(getResponse.code))
    print('Message: ' + str(getResponse.message))
    print('MoreResults: ' + str(getResponse.more_results))
    print('RequestID: ' + str(getResponse.request_id))
    print('Results Length: ' + str(len(getResponse.results)))
    # Since this could potentially return a large number of results, we do not want to print the results
    #print 'Results: ' + str(getResponse.results)

    while getResponse.more_results: 
        print('>>> Continue Retrieve Filtered OpenEvents with GetMoreResults')
        getResponse = getOpenEvent.getMoreResults()
        print('Retrieve Status: ' + str(getResponse.status))
        print('Code: ' + str(getResponse.code))
        print('Message: ' + str(getResponse.message))
        print('MoreResults: ' + str(getResponse.more_results))
        print('RequestID: ' + str(getResponse.request_id))
        print('Results Length: ' + str(len(getResponse.results)))
    
    #  The following request could potentially bring back large amounts of data if run against a production account
    '''
    print '>>> Retrieve All OpenEvents with GetMoreResults'
    getOpenEvent = ET_Client.ET_OpenEvent()
    getOpenEvent.auth_stub = stubObj
    getOpenEvent.props = ["SendID","SubscriberKey","EventDate","Client.ID","EventType","BatchID","TriggeredSendDefinitionObjectID","PartnerKey"]
    getResponse = getOpenEvent.get()
    print 'Retrieve Status: ' + str(getResponse.status)
    print 'Code: ' + str(getResponse.code)
    print 'Message: ' + str(getResponse.message)
    print 'MoreResults: ' + str(getResponse.more_results)
    print 'RequestID: ' + str(getResponse.request_id)
    print 'Results Length: ' + str(len(getResponse.results))
    # Since this could potentially return a large number of results, we do not want to print the results
    #print 'Results: ' + str(getResponse.results)
    
    while getResponse.more_results: 
        print '>>> Continue Retrieve All OpenEvents with GetMoreResults'
        getResponse = getOpenEvent.getMoreResults()
        print 'Retrieve Status: ' + str(getResponse.status)
        print 'Code: ' + str(getResponse.code)
        print 'Message: ' + str(getResponse.message)
        print 'MoreResults: ' + str(getResponse.more_results)
        print 'RequestID: ' + str(getResponse.request_id)
        print 'Results Length: ' + str(len(getResponse.results))
    '''

except Exception as e:
    print('Caught exception: ' + e.message)
    print(e)