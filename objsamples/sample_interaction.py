import ET_Client

try:
    debug = False
    stubObj = ET_Client.ET_Client(False, debug)
    
    # In order for this sample to run, it needs to have a interaction.
    SubscriberKey = "123456789"
    EventDefinitionKey = "ContactEvent-xxxxxxxx"

    # Event Fire for interaction
    print '>>> Event Fire for interaction'
    postInteractionEvent = ET_Client.ET_InteractionEvents()
    postInteractionEvent.auth_stub = stubObj
    postInteractionEvent.props = {
        "ContactKey": SubscriberKey,
        "EventDefinitionKey": EventDefinitionKey,
        "Data": {
            "Id":"01234567",
            "Foo":"Bar"
        }
    }
    postInteractionEventResponse = postInteractionEvent.post()

    print 'PostRequest Status: ' + str(postInteractionEventResponse.status)
    print 'Code: ' + str(postInteractionEventResponse.code)
    print 'eventInstanceId: ' + str(postInteractionEventResponse.results['eventInstanceId'])
    print '-----------------------------'

except Exception as e:
    print 'Caught exception: ' + e.message
    print e