import ET_Client

try:
    debug = False
    stubObj = ET_Client.ET_Client(False, debug)
    
    # In order for this sample to run, it needs to have an asset that it can associate the campaign to
    ExampleAssetType = "LIST"
    ExampleAssetItemID = "1953114"

    # Retrieve all Campaigns
    print('>>> Retrieve all Campaigns')
    getCamp = ET_Client.ET_Campaign()
    getCamp.auth_stub = stubObj
    getResponse = getCamp.get()
    print('Retrieve Status: ' + str(getResponse.status))
    print('Code: ' + str(getResponse.code))
    print('Message: ' + str(getResponse.message))
    print('MoreResults: ' + str(getResponse.more_results))
    if 'count' in getResponse.results:
        print('Results(Items) Length: ' + str(len(getResponse.results['items'])))
    # print 'Results(Items): ' + str(getResponse.results)
    print('-----------------------------')

    while getResponse.more_results:
        print('>>> Continue Retrieve all Campaigns with GetMoreResults')
        getResponse = getCamp.getMoreResults()
        print(str(getResponse))
        print('Retrieve Status: ' + str(getResponse.status))
        print('Code: ' + str(getResponse.code))
        print('Message: ' + str(getResponse.message))
        print('MoreResults: ' + str(getResponse.more_results))
        print('RequestID: ' + str(getResponse.request_id))
        if 'count' in getResponse.results:
            print('Results(Items) Length: ' + str(len(getResponse.results['items'])))

    # Create a new Campaign
    print('>>> Create a new Campaign')
    postCamp = ET_Client.ET_Campaign()
    postCamp.auth_stub = stubObj
    postCamp.props = {"name" : "PythonSDKCreatedForTest", "description": "PythonSDKCreatedForTest", "color":"FF9933", "favorite":"false"}
    postResponse = postCamp.post()
    print('Post Status: ' + str(postResponse.status))
    print('Code: ' + str(postResponse.code))
    print('Message: ' + str(postResponse.message))
    print('Results: ' + str(postResponse.results))
    print('-----------------------------')

    if postResponse.status:
    
        IDOfpostCampaign = postResponse.results['id']

        # Retrieve the new Campaign
        print('>>> Retrieve the new Campaign')
        getCamp = ET_Client.ET_Campaign()
        getCamp.auth_stub = stubObj
        getCamp.props = {"id" : IDOfpostCampaign}
        getResponse = getCamp.get()
        print('Retrieve Status: ' + str(getResponse.status))
        print('Code: ' + str(getResponse.code))
        print('Message: ' + str(getResponse.message))
        print('Results: ' + str(getResponse.results))
        print('-----------------------------')

        # Update the new Campaign
        print('>>> Update the new Campaign')
        patchCamp = ET_Client.ET_Campaign()
        patchCamp.auth_stub = stubObj
        patchCamp.props = {"id": IDOfpostCampaign, "name" : "PythonSDKCreated-Updated!"}
        postResponse = patchCamp.patch()
        print('Patch Status: ' + str(postResponse.status))
        print('Code: ' + str(postResponse.code))
        print('Message: ' + str(postResponse.message))
        print('Results: ' + str(postResponse.results))
        print('-----------------------------')
    
        # Retrieve the updated Campaign
        print('>>> Retrieve the updated Campaign')
        getCamp = ET_Client.ET_Campaign()
        getCamp.auth_stub = stubObj
        getCamp.props = {"id" : IDOfpostCampaign}
        getResponse = getCamp.get()
        print('Retrieve Status: ' + str(getResponse.status))
        print('Code: ' + str(getResponse.code))
        print('Message: ' + str(getResponse.message))
        print('Results: ' + str(getResponse.results))
        print('-----------------------------')

        # Create a new Campaign Asset
        print('>>> Create a new Campaign Asset')
        postCampAsset = ET_Client.ET_Campaign_Asset()
        postCampAsset.auth_stub = stubObj
        postCampAsset.props = {"id" : IDOfpostCampaign, "ids": [ExampleAssetItemID], "type": ExampleAssetType}
        postResponse = postCampAsset.post()
        print('Post Status: ' + str(postResponse.status))
        print('Code: ' + str(postResponse.code))
        print('Message: ' + str(postResponse.message))
        print('Results: ' + str(postResponse.results))
        print('-----------------------------')

        IDOfpostCampaignAsset = postResponse.results[0]['id']

        # Retrieve all Campaign Asset for a campaign
        print('>>> Retrieve all Campaign Asset for a Campaign')
        getCampAsset = ET_Client.ET_Campaign_Asset()
        getCampAsset.auth_stub = stubObj
        getCampAsset.props = {"id" : IDOfpostCampaign}
        getResponse = getCampAsset.get()
        print('Retrieve Status: ' + str(getResponse.status))
        print('Code: ' + str(getResponse.code))
        print('Message: ' + str(getResponse.message))
        print('Results: ' + str(getResponse.results))
        print('-----------------------------')

        # Retrieve a single new Campaign Asset
        print('>>> Retrieve a single new Campaign Asset')
        getCampAsset = ET_Client.ET_Campaign_Asset()
        getCampAsset.auth_stub = stubObj
        getCampAsset.props = {"id" : IDOfpostCampaign, "assetId" : IDOfpostCampaignAsset}
        getResponse = getCampAsset.get()
        print('Retrieve Status: ' + str(getResponse.status))
        print('Code: ' + str(getResponse.code))
        print('Message: ' + str(getResponse.message))
        print('Results: ' + str(getResponse.results))
        print('-----------------------------')

        # Delete the new Campaign Asset
        print('>>> Delete the new Campaign Asset')
        deleteCampAsset = ET_Client.ET_Campaign_Asset()
        deleteCampAsset.auth_stub = stubObj
        deleteCampAsset.props = {"id" : IDOfpostCampaign, "assetId": IDOfpostCampaignAsset}
        deleteResponse = deleteCampAsset.delete()
        print('Delete Status: ' + str(deleteResponse.status))
        print('Code: ' + str(deleteResponse.code))
        print('Message: ' + str(deleteResponse.message))
        print('Results: ' + str(deleteResponse.results))
        print('-----------------------------')

        # Get a single a new Campaign Asset to confirm deletion
        print('>>> Get a single a new Campaign Asset to confirm deletion')
        getCampAsset = ET_Client.ET_Campaign_Asset()
        getCampAsset.auth_stub = stubObj
        getCampAsset.props = {"id" : IDOfpostCampaign, "assetId" : IDOfpostCampaignAsset}
        getResponse = getCampAsset.get()
        print('Retrieve Status: ' + str(getResponse.status))
        print('Code: ' + str(getResponse.code))
        print('Message: ' + str(getResponse.message))
        print('Results: ' + str(getResponse.results))
        print('-----------------------------')

        # Delete the new Campaign
        print('>>> Delete the new Campaign')
        deleteCamp = ET_Client.ET_Campaign()
        deleteCamp.auth_stub = stubObj
        deleteCamp.props = {"id": IDOfpostCampaign}
        deleteResponse = deleteCamp.delete()
        print('Delete Status: ' + str(deleteResponse.status))
        print('Code: ' + str(deleteResponse.code))
        print('Message: ' + str(deleteResponse.message))
        print('Results: ' + str(deleteResponse.results))
        print('-----------------------------')

except Exception as e:
    print('Caught exception: ' + e.message)
    print(e)