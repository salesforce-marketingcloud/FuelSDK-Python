import ET_Client
import uuid

try:
    debug = False
    stubObj = ET_Client.ET_Client(False, debug)

    # Get all TriggeredSendDefinitions
    print('>>> Get all TriggeredSendDefinitions')
    getTS = ET_Client.ET_TriggeredSend()
    getTS.auth_stub = stubObj
    getTS.props = ["CustomerKey", "Name", "TriggeredSendStatus"]
    getResponse = getTS.get()
    print('Retrieve Status: ' + str(getResponse.status))
    print('Code: ' + str(getResponse.code))
    print('Message: ' + str(getResponse.message))
    print('MoreResults: ' + str(getResponse.more_results))
    print('Results Count: ' + str(len(getResponse.results)))
    #print 'Results: ' + str(getResponse.results)
            
    # Specify the name of a TriggeredSend that was setuprint for testing 
    # Do not use a production Triggered Send Definition

    NameOfTestTS = "TEXTEXT"
    
    # Pause a TriggeredSend
    
    print('>>> Pause a TriggeredSend')
    patchTrig = ET_Client.ET_TriggeredSend()
    patchTrig.auth_stub = stubObj
    patchTrig.props = {"CustomerKey" : NameOfTestTS, "TriggeredSendStatus" :"Inactive"}
    patchResponse = patchTrig.patch()
    print('Patch Status: ' + str(patchResponse.status))
    print('Code: ' + str(patchResponse.code))
    print('Message: ' + str(patchResponse.message))
    print('Result Count: ' + str(len(patchResponse.results)))
    print('Results: ' + str(patchResponse.results))
    
    
    # Retrieve Single TriggeredSend
    print('>>> Retrieve Single TriggeredSend')
    getTS = ET_Client.ET_TriggeredSend()
    getTS.auth_stub = stubObj
    getTS.props = ["CustomerKey", "Name", "TriggeredSendStatus"]
    getTS.search_filter = {'Property' : 'CustomerKey','SimpleOperator' : 'equals','Value' : NameOfTestTS}
    getResponse = getTS.get()
    print('Retrieve Status: ' + str(getResponse.status))
    print('Code: ' + str(getResponse.code))
    print('Message: ' + str(getResponse.message))
    print('MoreResults: ' + str(getResponse.more_results))
    print('Results Count: ' + str(len(getResponse.results)))
    print('Results: ' + str(getResponse.results))
    
    # Start a TriggeredSend by setting to Active
    print('>>> Start a TriggeredSend by setting to Active')
    patchTrig = ET_Client.ET_TriggeredSend()
    patchTrig.auth_stub = stubObj
    patchTrig.props = {"CustomerKey" : NameOfTestTS, "TriggeredSendStatus" :"Active"}
    patchResponse = patchTrig.patch()
    print('Patch Status: ' + str(patchResponse.status))
    print('Code: ' + str(patchResponse.code))
    print('Message: ' + str(patchResponse.message))
    print('Result Count: ' + str(len(patchResponse.results)))
    print('Results: ' + str(patchResponse.results))
    
    # Retrieve Single TriggeredSend After setting back to active
    print('>>> Retrieve Single TriggeredSend After setting back to active')
    getTS = ET_Client.ET_TriggeredSend()
    getTS.auth_stub = stubObj
    getTS.props = ["CustomerKey", "Name", "TriggeredSendStatus"]
    getTS.search_filter = {'Property' : 'CustomerKey','SimpleOperator' : 'equals','Value' : NameOfTestTS}
    getResponse = getTS.get()
    print('Retrieve Status: ' + str(getResponse.status))
    print('Code: ' + str(getResponse.code))
    print('Message: ' + str(getResponse.message))
    print('MoreResults: ' + str(getResponse.more_results))
    print('Results Count: ' + str(len(getResponse.results)))
    print('Results: ' + str(getResponse.results))
    
    
    # Send an email with TriggeredSend
    print('>>> Send an email with TriggeredSend')
    sendTrig = ET_Client.ET_TriggeredSend()
    sendTrig.auth_stub = stubObj
    sendTrig.props = {"CustomerKey" : NameOfTestTS}
    sendTrig.subscribers = [{"EmailAddress":"testing@bh.exacttarget.com", "SubscriberKey" : "testing@bh.exacttarget.com"}]
    sendResponse = sendTrig.send()
    print('Send Status: ' + str(sendResponse.status))
    print('Code: ' + str(sendResponse.code))
    print('Message: ' + str(sendResponse.message))
    print('Result Count: ' + str(len(sendResponse.results)))
    print('Results: ' + str(sendResponse.results))
    
    # Generate a unique identifier for the TriggeredSend customer key since they cannot be re-used even after deleted
    TSNameForCreateThenDelete = str(uuid.uuid4())
    
    # Create a TriggeredSend Definition 
    print('>>> Create a TriggeredSend Definition')
    postTrig = ET_Client.ET_TriggeredSend()
    postTrig.auth_stub = stubObj
    postTrig.props = {'CustomerKey' : TSNameForCreateThenDelete,'Name' : TSNameForCreateThenDelete, 'Email' : {"ID":"3113962"}, "SendClassification": {"CustomerKey": "2240"}}
    postResponse = postTrig.post()
    print('Post Status: ' + str(postResponse.status))
    print('Code: ' + str(postResponse.code))
    print('Message: ' + str(postResponse.message))
    print('Result Count: ' + str(len(postResponse.results)))
    print('Results: ' + str(postResponse.results))
    
    # Delete a TriggeredSend Definition 
    print('>>> Delete a TriggeredSend Definition ')
    deleteTrig = ET_Client.ET_TriggeredSend()
    deleteTrig.auth_stub = stubObj
    deleteTrig.props = {'CustomerKey' : TSNameForCreateThenDelete}
    deleteResponse = deleteTrig.delete()
    print('Delete Status: ' + str(deleteResponse.status))
    print('Code: ' + str(deleteResponse.code))
    print('Message: ' + str(deleteResponse.message))
    print('Result Count: ' + str(len(deleteResponse.results)))
    print('Results: ' + str(deleteResponse.results))

except Exception as e:
    print('Caught exception: ' + e.message)
    print(e)