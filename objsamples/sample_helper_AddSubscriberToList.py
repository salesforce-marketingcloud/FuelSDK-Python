import sys
sys.path.append("../")
import ET_Client

try:
    debug = False
    stubObj = ET_Client.ET_Client(False, debug)
    
    NewListName = "RubySDKList"

    ## Example using AddSubscriberToList() method
    ## Typically this method will be used with a pre-existing list but for testing purposes one is being created.
    
    # Create List 
    print '>>> Create List'
    postList = ET_Client.ET_List()
    postList.authStub = stubObj
    postList.props = {"ListName" : NewListName, "Description" : "This list was created with the RubySDK", "Type" : "Private" }
    postResponse = postList.post()
    print 'Post Status: ' + str(postResponse.status)
    print 'Code: ' + str(postResponse.code)
    print 'Message: ' + str(postResponse.message)
    print 'Result Count: ' + str(postResponse.results.length)
    print 'Results: ' + str(postResponse.results.inspect)
    
    if postResponse.status then 
        
        newListID = postResponse.results[0][:new_id]
        # Adding Subscriber To a List
        print '>>> Add Subscriber To a List'
        AddSubResponse = stubObj.AddSubscriberToList("AddSubTesting@bh.exacttarget.com", [newListID])
        print 'AddSubResponse Status: ' + str(AddSubResponse.status)
        print 'Code: ' + str(AddSubResponse.code)
        print 'Message: ' + str(AddSubResponse.message)
        print 'Result Count: ' + str(AddSubResponse.results.length)
        print 'Results: ' + str(AddSubResponse.results.inspect)
                
        # Delete List
        print '>>> Delete List'
        deleteSub = ET_Client.ET_List()
        deleteSub.authStub = stubObj
        deleteSub.props = {"ID" : newListID}
        deleteResponse = deleteSub.delete
        print 'Delete Status: ' + str(deleteResponse.status)
        print 'Code: ' + str(deleteResponse.code)
        print 'Message: ' + str(deleteResponse.message)
        print 'Results Length: ' + str(deleteResponse.results.length)
        print 'Results: ' + str(deleteResponse.results)

except Exception as e:
    print 'Caught exception: ' + e.message
    print e