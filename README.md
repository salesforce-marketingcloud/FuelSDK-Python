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

The quickest way to install the required libraries is to use pip and tell it to load the libraries listed in the requiredlibraries.txt file (see below). Pip is a tool for installing and managing Python packages and is available at https://pypi.python.org/pypi/pip.

pip install -r requirements.txt


## Getting Started ##
### Custom Suds Changes ###
The default Suds 0.4 Package that is available for download needs to have a couple small fixes applied in order for it to fully support the Fuel SDK. Please update your suds installation using the following instructions:

- Download the suds package source from https://pypi.python.org/pypi/suds
- Open the file located wihin the uncompressed files at: suds\mx\appender.py
- At line 223, the following lines will be present:
><pre>
        child.setText(p.get())
        parent.append(child)
        for item in p.items():
            cont = Content(tag=item[0], value=item[1])
            Appender.append(self, child, cont)
</pre>

- Replace those lines with:
><pre>
        child_value = p.get()
        if(child_value is None):
            pass
        else:
            child.setText(child_value)
            parent.append(child)
            for item in p.items():
                cont = Content(tag=item[0], value=item[1])
                Appender.append(self, child, cont)

</pre>

- Open the file located wihin the uncompressed files at suds\bindings\document.py
- After line 62 which reads:
><pre>
            n += 1
</pre>

- Add the following lines: 
><pre>
            if value is None:
                continue
</pre>
- Install Suds by running the command
> python setup.py install


### Configuring ###
After downloading the project, rename the config.python.template file to config.python. 

Edit config.python so you can input the ClientID and Client Secret values provided when you registered your application. If you are building a HubExchange application for the Interactive Marketing Hub then, you must also provide the Application Signature (appsignature).  Only change the value for the defaultwsdl configuration item if instructed by ExactTarget.

If you have not registered your application or you need to lookup your Application Key or Application Signature values, please go to App Center at [Code@: ExactTarget's Developer Community](http://code.exacttarget.com/appcenter "Code@ App Center").

## Example Request ##
All ExactTarget objects exposed through the Fuel SDK begin with be prefixed with "ET\_".  Start by working with the ET_List object:

Add a require statement to reference the Fuel SDK's functionality:
> import FuelSDK

Next, create an instance of the ET_Client class:
> myClient = FuelSDK.ET_Client()

Create an instance of the object type we want to work with:
> list = FuelSDK.ET_List()

Associate the ET_Client to the object using the auth_stub property:
> list.auth_stub = myClient

Utilize one of the ET_List methods:
> response = list.get()

Print out the results for viewing
> print 'Post Status: ' + str(response.status) <br />
print 'Code: ' + str(response.code) <br />
print 'Message: ' + str(response.message) <br />
print 'Result Count: ' + str(len(response.results)) <br />
print 'Results: ' + str(response.results)


**Example Output:**

<pre>
Retrieve Status: True
Code: 200
Message: OK
MoreResults: False
Results Length: 1
Results: [(List){
   Client =
      (ClientID){
         ID = 113903
      }
   PartnerKey = None
   CreatedDate = 2013-07-29 04:43:32.000073
   ModifiedDate = 2013-07-29 04:43:32.000073
   ID = 1966872
   ObjectID = None
   CustomerKey = "343431CD-031D-43C7-981F-51B778A5A47F"
   ListName = "PythonSDKList"
   Category = 578615
   Type = "Private"
   Description = "This list was created with the PythonSDK"
   ListClassification = "ExactTargetList"
 }]
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

 - [BounceEvent](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample_bounceevent.py)
 - [Campaign](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample_campaign.py)
 - [ClickEvent](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample_clickevent.py)
 - [ContentArea](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample_contentarea.py)
 - [DataExtension](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample_dataextension.py)
 - [Email](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample_email.py)
 - [List](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample_list.py)
 - [List > Subscriber](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample_subscriber.py)
 - [OpenEvent](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample_openevent.py)
 - [SentEvent](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample_sentevent.py)
 - [Subscriber](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample_subscriber.py)
 - [TriggeredSend](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample_triggeredsend.py)
 - [UnsubEvent](https://github.com/ExactTarget/FuelSDK-Python/blob/master/objsamples/sample_unsubevent.py)

## Copyright and license ##
Copyright (c) 2013 ExactTarget

Licensed under the MIT License (the "License"); you may not use this work except in compliance with the License. You may obtain a copy of the License in the COPYING file.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

 



