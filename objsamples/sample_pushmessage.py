import ET_Client

try:
    debug = False
    stubObj = ET_Client.ET_Client(False, debug)
    
    # In order for this sample to run, it needs to have a message for mobile push and a mobile push contact.
    SubscriberKey = "test"
    MessageID = "NDAxxxxxx"

    # Push Message for contact
    print '>>> Push Message for contact'
    pushMessageContact = ET_Client.ET_PushMessageContact()
    pushMessageContact.auth_stub = stubObj
    pushMessageContact.props = {"messageId": MessageID, "SubscriberKeys": [SubscriberKey]}
    pushMessageContactResponse = pushMessageContact.post()

    print 'PushMessageRequest Status: ' + str(pushMessageContactResponse.status)
    print 'Code: ' + str(pushMessageContactResponse.code)
    print 'tokenId: ' + str(pushMessageContactResponse.results['tokenId'])
    print '-----------------------------'

    # Get a delivery information for mobile push message
    print '>>> Get a delivery information for mobile push message'
    getPushMessageDelivery = ET_Client.ET_PushMessageContact_Deliveries()
    getPushMessageDelivery.auth_stub = stubObj
    getPushMessageDelivery.props = {
        "messageId" : MessageID, 
        "tokenId" : pushMessageContactResponse.results['tokenId']
    }
    getPushMessageDeliveryResponse = getPushMessageDelivery.get()
    print 'GetRequest Status: ' + str(getPushMessageDeliveryResponse.status)
    print 'Code: ' + str(getPushMessageDeliveryResponse.code)
    print 'Results: ' + str(getPushMessageDeliveryResponse.results)
    print 'Message: ' + str(getPushMessageDeliveryResponse.results['message'])
    print 'CreateDate: ' + str(getPushMessageDeliveryResponse.results['createDate'])
    print '-----------------------------'

except Exception as e:
    print 'Caught exception: ' + e.message
    print e