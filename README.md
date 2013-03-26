FuelSDK-Python
============

ExactTarget Fuel SDK for Python

## Overview ##
The Fuel SDK for Python provides easy access to ExactTarget's Fuel API Family services, including a collection of REST APIs and a SOAP API. These APIs provide access to ExactTarget functionality via common collection types such as array/hash. 

## Requirements ##
Python 2.7.3

libraries:

- pyjwt 0.1.5
- requests 1.1.0
- suds 0.4


## Getting Started ##
After downloading the project, rename the config.python.template file to config.python. 

Edit config.python so you can input the ClientID and Client Secret values provided when you registered your application. If you are building a HubExchange application for the Interactive Marketing Hub then, you must also provide the Application Signature (appsignature).  Only change the value for the defaultwsdl configuration item if instructed by ExactTarget.

If you have not registered your application or you need to lookup your Application Key or Application Signature values, please go to App Center at [Code@: ExactTarget's Developer Community](http://code.exacttarget.com/appcenter "Code@ App Center").

## Example Request ##
All ExactTarget objects exposed through the Fuel SDK begin with be prefixed with "ET\_".  Start by working with the ET_List object:

Add a require statement to reference the Fuel SDK's functionality:
> import 'ET_Client'

Next, create an instance of the ET_Client class:
> myClient = ET_Client.ET_Client()

Create an instance of the object type we want to work with:
> list = ET_List()

Associate the ET_Client to the object using the authStub property:
> list.authStub = myClient

Utilize one of the ET_List methods:
> response = list.get()

Print out the results for viewing
> print response

**Example Output:**

<pre>
#&lt;ET_Get:0x355bc48 
	@results=[
		{
			:client=>{
				:id=>"1000001", 
				:partner_client_key=>nil
				}, 
			:partner_key=>nil, 
			:created_date=>#&lt;DateTime: 2009-06-12T14:42:06+00:00 ((2454995j,52926s,100000000n),+0s,2299161j)&gt;, 
			:modified_date=>#&lt;DateTime: 2011-08-17T14:50:30+00:00 ((2455791j,53430s,697000000n),+0s,2299161j)&gt;, 
			:id=>"1718921", 
			:object_id=>"f41c7d1b-8957-de11-92ee-001cc494ae9e", 
			:customer_key=>"All Subscribers - 578623", 
			:list_name=>"All Subscribers", 
			:category=>"578623", 
			:type=>"Private", 
			:description=>"Contains all subscribers", 
			:list_classification=>"ExactTargetList", 
			:"@xsi:type"=>"List"}
		], 
	@code=200, 
	@status=true, 
	@moreResults=false, 
	@request_id="41f0f293-954f-4ac7-8e7a-0a5756022218"
>
</pre>

## ET\_Client Class ##

The ET\_Client class takes care of many of the required steps when accessing ExactTarget's API, including retrieving appropriate access tokens, handling token state for managing refresh, and determining the appropriate endpoints for API requests.  In order to leverage the advantages this class provides, use a single instance of this class for an entire session.  Do not instantiate a new ET_Client object for each request made. 

## Responses ##
All methods on Fuel SDK objects return a generic object that follows the same structure, regardless of the type of call.  This object contains a common set of properties used to display details about the request.

- status: Boolean value that indicates if the call was successful
- code: HTTP Error Code (will always be 200 for SOAP requests)
- message: Text values containing more details in the event of an error
- results: Collection containing the details unique to the method called. 

Get Methods also return an addition value to indicate if more information is available (that information can be retrieved using the getMoreResults method):

 - moreResults - Boolean value that indicates on Get requests if more data is available. 


## Samples ##
Find more sample files that illustrate using all of the available functions for ExactTarget objects exposed through the API in the objsamples directory. 

Sample List:

 - [BounceEvent](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample-bounceevent.py)
 - [Campaign](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample-campaign.py)
 - [ClickEvent](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample-clickevent.py)
 - [ContentArea](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample-contentarea.py)
 - [DataExtension](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample-dataextension.py)
 - [Email](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample-email.py)
 - [List](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample-list.py)
 - [List > Subscriber](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample-subscriber.py)
 - [OpenEvent](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample-openevent.py)
 - [SentEvent](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample-sentevent.py)
 - [Subscriber](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample-subscriber.py)
 - [TriggeredSend](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample-triggeredsend.py)
 - [UnsubEvent](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample-unsubevent.py)


 



