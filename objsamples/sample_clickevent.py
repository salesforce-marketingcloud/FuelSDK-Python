import ET_Client

try:
    debug = False
    stubObj = ET_Client.ET_Client(False, debug)
        
    ## Modify the date below to reduce the number of results returned from the request
    ## Setting this too far in the past could result in a very large response size
    retrieveDate = '2013-01-15T13:00:00.000'

    print('>>> Retrieve Filtered ClickEvents with GetMoreResults')
    getClickEvent = ET_Client.ET_ClickEvent()
    getClickEvent.auth_stub = stubObj   
    getClickEvent.props = ["SendID","SubscriberKey","EventDate","Client.ID","EventType","BatchID","TriggeredSendDefinitionObjectID","PartnerKey"]
    getClickEvent.search_filter = {'Property' : 'EventDate','SimpleOperator' : 'greaterThan','DateValue' : retrieveDate}
    getResponse = getClickEvent.get()
    print('Retrieve Status: ' + str(getResponse.status))
    print('Code: ' + str(getResponse.code))
    print('Message: ' + str(getResponse.message))
    print('MoreResults: ' + str(getResponse.more_results))
    print('RequestID: ' + str(getResponse.request_id))
    print('Results Length: ' + str(len(getResponse.results)))
    # Since this could potentially return a large number of results, we do not want to print the results
    #print 'Results: ' + getResponse.results.to_s

    while getResponse.more_results: 
        print('>>> Continue Retrieve Filtered ClickEvents with GetMoreResults')
        getResponse = getClickEvent.getMoreResults()
        print('Retrieve Status: ' + str(getResponse.status))
        print('Code: ' + str(getResponse.code))
        print('Message: ' + str(getResponse.message))
        print('MoreResults: ' + str(getResponse.more_results))
        print('RequestID: ' + str(getResponse.request_id))
        print('Results Length: ' + str(len(getResponse.results)))
    
    #  The following request could potentially bring back large amounts of data if run against a production account 
    '''
    print '>>> Retrieve All ClickEvents with GetMoreResults'
    getClickEvent = ET_ClickEvent.new()
    getClickEvent.auth_stub = stubObj   
    getClickEvent.props = ["SendID","SubscriberKey","EventDate","Client.ID","EventType","BatchID","TriggeredSendDefinitionObjectID","PartnerKey"]   
    getResponse = getClickEvent.get()
    print 'Retrieve Status: ' + str(getResponse.status)
    print 'Code: ' + str(getResponse.code)
    print 'Message: ' + str(getResponse.message)
    print 'MoreResults: ' + str(getResponse.more_results)
    print 'RequestID: ' + str(getResponse.request_id)
    print 'Results Length: ' + str(len(getResponse.results))
    # Since this could potentially return a large number of results, we do not want to print the results
    #print 'Results: ' + getResponse.results.to_s
    
    while getResponse.more_results:
        print '>>> Continue Retrieve All ClickEvents with GetMoreResults'
        getResponse = getClickEvent.getMoreResults()
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

