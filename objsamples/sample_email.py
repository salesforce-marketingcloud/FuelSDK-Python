import sys
sys.path.append("../")
import ET_Client

try:
    debug = False
    stubObj = ET_Client.ET_Client(False, debug)
    
    # Retrieve All Email with GetMoreResults
    print '>>> Retrieve All Email with GetMoreResults'
    getHTMLBody = ET_Client.ET_Email()
    getHTMLBody.authStub = stubObj
    getHTMLBody.props = ["ID","PartnerKey","CreatedDate","ModifiedDate","Client.ID","Name","Folder","CategoryID","HTMLBody","TextBody","Subject","IsActive","IsHTMLPaste","ClonedFromID","Status","EmailType","CharacterSet","HasDynamicSubjectLine","ContentCheckStatus","Client.PartnerClientKey","ContentAreas","CustomerKey"]
    getResponse = getHTMLBody.get()
    print 'Retrieve Status: ' + str(getResponse.status)
    print 'Code: ' + str(getResponse.code)
    print 'Message: ' + str(getResponse.message)
    print 'MoreResults: ' + str(getResponse.more_results)
    print 'Results Length: ' + str(len(getResponse.results))
    #print 'Results: ' + str(getResponse.results)

    while getResponse.more_results: 
        print '>>> Continue Retrieve All Email with GetMoreResults'
        getResponse = getHTMLBody.getMoreResults()
        print 'Retrieve Status: ' + str(getResponse.status)
        print 'Code: ' + str(getResponse.code)
        print 'Message: ' + str(getResponse.message)
        print 'MoreResults: ' + str(getResponse.more_results)
        print 'RequestID: ' + str(getResponse.request_id)
        print 'Results Length: ' + str(len(getResponse.results))

    NameOfTestEmail = "RubySDKEmail"

    # Create Email 
    print '>>> Create Email'
    postHTMLBody = ET_Client.ET_Email()
    postHTMLBody.authStub = stubObj
    postHTMLBody.props = {"CustomerKey" : NameOfTestEmail, "Name":NameOfTestEmail, "Subject" : "Created Using the RubySDK", "HTMLBody": "<b>Some HTML Goes here</b>"}
    postResponse = postHTMLBody.post()
    print 'Post Status: ' + str(postResponse.status)
    print 'Code: ' + str(postResponse.code)
    print 'Message: ' + str(postResponse.message)
    print 'Result Count: ' + str(postResponse.results.length)
    print 'Results: ' + str(postResponse.results.inspect)

    # Retrieve newly created Email
    print '>>> Retrieve newly created Email'
    getHTMLBody = ET_Client.ET_Email()
    getHTMLBody.authStub = stubObj
    getHTMLBody.props = ["ID","PartnerKey","CreatedDate","ModifiedDate","Client.ID","Name","Folder","CategoryID","HTMLBody","TextBody","Subject","IsActive","IsHTMLPaste","ClonedFromID","Status","EmailType","CharacterSet","HasDynamicSubjectLine","ContentCheckStatus","Client.PartnerClientKey","ContentAreas","CustomerKey"]
    getHTMLBody.search_filter = {'Property' : 'CustomerKey','SimpleOperator' : 'equals','Value' : NameOfTestEmail}
    getResponse = getHTMLBody.get()
    print 'Retrieve Status: ' + str(getResponse.status)
    print 'Code: ' + str(getResponse.code)
    print 'Message: ' + str(getResponse.message)
    print 'MoreResults: ' + str(getResponse.more_results)
    print 'Results Length: ' + str(len(getResponse.results))
    print 'Results: ' + str(getResponse.results)
    
    # Update Email 
    print '>>> Update Email'
    patchHTMLBody = ET_Client.ET_Email()
    patchHTMLBody.authStub = stubObj
    patchHTMLBody.props = {"CustomerKey" : NameOfTestEmail, "Name":NameOfTestEmail,  "HTMLBody": "<b>Some HTML HTMLBody Goes here. NOW WITH NEW HTMLBody</b>"}
    patchResponse = patchHTMLBody.patch
    print 'Patch Status: ' + str(postResponse.status)
    print 'Code: ' + str(postResponse.code)
    print 'Message: ' + str(postResponse.message)
    print 'Result Count: ' + str(postResponse.results.length)
    print 'Results: ' + str(postResponse.results.inspect)

    # Retrieve updated Email
    print '>>> Retrieve updated Email'
    getHTMLBody = ET_Client.ET_Email()
    getHTMLBody.authStub = stubObj
    getHTMLBody.props = ["ID","PartnerKey","CreatedDate","ModifiedDate","Client.ID","Name","Folder","CategoryID","HTMLBody","TextBody","Subject","IsActive","IsHTMLPaste","ClonedFromID","Status","EmailType","CharacterSet","HasDynamicSubjectLine","ContentCheckStatus","Client.PartnerClientKey","ContentAreas","CustomerKey"]
    getHTMLBody.search_filter = {'Property' : 'CustomerKey','SimpleOperator' : 'equals','Value' : NameOfTestEmail}
    getResponse = getHTMLBody.get()
    print 'Retrieve Status: ' + str(getResponse.status)
    print 'Code: ' + str(getResponse.code)
    print 'Message: ' + str(getResponse.message)
    print 'MoreResults: ' + str(getResponse.more_results)
    print 'Results Length: ' + str(len(getResponse.results))
    print 'Results: ' + str(getResponse.results)
    
    # Delete Email 
    print '>>> Delete Email'
    deleteHTMLBody = ET_Client.ET_Email()
    deleteHTMLBody.authStub = stubObj
    deleteHTMLBody.props = {"CustomerKey" : NameOfTestEmail, "Name":NameOfTestEmail, "HTMLBody": "<b>Some HTML HTMLBody Goes here. NOW WITH NEW HTMLBody</b>"}
    deleteResponse = deleteHTMLBody.delete
    print 'Delete Status: ' + str(deleteResponse.status)
    print 'Code: ' + str(deleteResponse.code)
    print 'Message: ' + str(deleteResponse.message)
    print 'Result Count: ' + str(deleteResponse.results.length)
    print 'Results: ' + str(deleteResponse.results.inspect)
    
    # Retrieve Email to confirm deletion
    print '>>> Retrieve Email to confirm deletion'
    getHTMLBody = ET_Client.ET_Email()
    getHTMLBody.authStub = stubObj
    getHTMLBody.props = ["ID","PartnerKey","CreatedDate","ModifiedDate","Client.ID","Name","Folder","CategoryID","HTMLBody","TextBody","Subject","IsActive","IsHTMLPaste","ClonedFromID","Status","EmailType","CharacterSet","HasDynamicSubjectLine","ContentCheckStatus","Client.PartnerClientKey","ContentAreas","CustomerKey"]
    getHTMLBody.search_filter = {'Property' : 'CustomerKey','SimpleOperator' : 'equals','Value' : NameOfTestEmail}
    getResponse = getHTMLBody.get()
    print 'Retrieve Status: ' + str(getResponse.status)
    print 'Code: ' + str(getResponse.code)
    print 'Message: ' + str(getResponse.message)
    print 'MoreResults: ' + str(getResponse.more_results)
    print 'Results Length: ' + str(len(getResponse.results))
    print 'Results: ' + str(getResponse.results)

except Exception as e:
    print 'Caught exception: ' + e.message
    print e