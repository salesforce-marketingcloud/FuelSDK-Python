# FuelSDK-Python v1.3.0

Salesforce Marketing Cloud Fuel SDK for Python

## Overview

The Fuel SDK for Python provides easy access to Salesforce Marketing Cloud's Fuel API Family services, including a collection of REST APIs and a SOAP API. These APIs provide access to Salesforce Marketing Cloud functionality via common collection types such as array/hash.

New Features in Version 1.3.1
------------
* Removed dependency on suds-jurko due to setuptools>=58.0.0 not supporting 2to3, pointed to suds-community
* Removed wsgiref because it is part of the standard lib
* Removed distribute as it is part of setuptools.


New Features in Version 1.3.0
------------
* Added Refresh Token support for OAuth2 authentication
* Added Web/Public App support for OAuth2 authentication

   More details on Access Tokens for Web/Public Apps can be found [here](https://developer.salesforce.com/docs/atlas.en-us.mc-app-development.meta/mc-app-development/access-token-app.htm)

   Sample config:
   
   ```
  [Web Services]
  appsignature: none
  clientid: <CLIENT_ID>
  clientsecret: <CLIENT_SECRET>
  defaultwsdl: https://webservice.exacttarget.com/etframework.wsdl
  authenticationurl: <AUTH TENANT SPECIFIC ENDPOINT>
  baseapiurl: <REST TENANT SPECIFIC ENDPOINT>
  soapendpoint: <SOAP TENANT SPECIFIC ENDPOINT>
  wsdl_file_local_loc: <WSDL_PATH>/ExactTargetWSDL.xml
  
  [Auth Service]
  useOAuth2Authentication: True
  accountId: <TARGET_ACCOUNT_ID>
  scope: <PERMISSION_LIST>
  applicationType: <APPLICATION_TYPE>
  redirectURI: <REDIRECT_URI_FOR_PUBLIC/WEB_APP>
  authorizationCode: <AUTHORIZATION_CODE_FOR_PUBLIC/WEB_APP>
  ```

  Example passing config as a parameter to ET_Client constructor:
  
  ```
  stubObj = ET_Client.ET_Client(
    False, False,
    {
        'clientid': '<CLIENT_ID>',
        'clientsecret': '<CLIENT_SECRET>',
        'defaultwsdl': 'https://webservice.exacttarget.com/etframework.wsdl',
        'authenticationurl': '<AUTH TENANT SPECIFIC ENDPOINT>',
        'baseapiurl': '<REST TENANT SPECIFIC ENDPOINT>',
        'soapendpoint': '<SOAP TENANT SPECIFIC ENDPOINT>',
        'wsdl_file_local_loc': r'<WSDL_PATH>/ExactTargetWSDL.xml',
        'useOAuth2Authentication': 'True',
        'accountId': '<TARGET_ACCOUNT_ID>',
        'scope': '<PERMISSION_LIST>'
        'applicationType': '<APPLICATION_TYPE>'
        'redirectURI': '<REDIRECT_URI_FOR_PUBLIC/WEB_APP>'
        'authorizationCode': '<AUTHORIZATION_CODE_FOR_PUBLIC/WEB_APP>'
    })
  ```
  
* applicationType can have one of the following values: `server`, `public`, `web`. The default value of applicationType is `server`.
  
New Features in Version 1.2.0
------------
* Added support for OAuth2 authentication - [More Details](https://developer.salesforce.com/docs/atlas.en-us.mc-app-development.meta/mc-app-development/integration-considerations.htm)

  To enable OAuth2 authentication, set `useOAuth2Authentication: True` in the config.python file or pass it in the params argument to the ET_Client constructor.
  
  Sample Config for OAuth2:
  
  ```
  [Web Services]
  appsignature: none
  clientid: <CLIENT_ID>
  clientsecret: <CLIENT_SECRET>
  defaultwsdl: https://webservice.exacttarget.com/etframework.wsdl
  authenticationurl: <AUTH TENANT SPECIFIC ENDPOINT>
  baseapiurl: <REST TENANT SPECIFIC ENDPOINT>
  soapendpoint: <SOAP TENANT SPECIFIC ENDPOINT>
  wsdl_file_local_loc: <WSDL_PATH>/ExactTargetWSDL.xml
  
  [Auth Service]
  useOAuth2Authentication: True
  accountId: <TARGET_ACCOUNT_ID>
  scope: <PERMISSION_LIST>
  ```
  
  Example passing config as a parameter to ET_Client constructor:
  
  ```
  stubObj = ET_Client.ET_Client(
    False, False,
    {
        'clientid': '<CLIENT_ID>',
        'clientsecret': '<CLIENT_SECRET>',
        'defaultwsdl': 'https://webservice.exacttarget.com/etframework.wsdl',
        'authenticationurl': '<AUTH TENANT SPECIFIC ENDPOINT>',
        'baseapiurl': '<REST TENANT SPECIFIC ENDPOINT>',
        'soapendpoint': '<SOAP TENANT SPECIFIC ENDPOINT>',
        'wsdl_file_local_loc': r'<WSDL_PATH>/ExactTargetWSDL.xml',
        'useOAuth2Authentication': 'True',
        'accountId': '<TARGET_ACCOUNT_ID>',
        'scope': '<PERMISSION_LIST>'
    })
  ```

New Features in Version 1.1.1 
------------
* Added support for your tenant’s endpoints - [More Details](https://developer.salesforce.com/docs/atlas.en-us.mc-apis.meta/mc-apis/your-subdomain-tenant-specific-endpoints.htm)

## Installation

The Fuel SDK for python can be easily installed from the [Python Package Index](https://pypi.python.org/pypi) using the [pip](https://pip.readthedocs.org) command. Pip is a tool for installing and managing Python packages.

```
pip install Salesforce-FuelSDK
```

## Getting Started

### Configuring

You must configure your access tokens and details for the Fuel SDK in one of the following two ways.

1. Copy the included `config.python.template` file to `config.python` in either `~/.fuelsdk/` or within this python module.
2. Add environment variables:
    * `FUELSDK_CLIENT_ID` (required)
    * `FUELSDK_CLIENT_SECRET` (required)
    * `FUELSDK_APP_SIGNATURE`
    * `FUELSDK_DEFAULT_WSDL`
    * `FUELSDK_BASE_API_URL`
    * `FUELSDK_AUTH_URL`
    * `FUELSDK_SOAP_ENDPOINT`
    * `FUELSDK_WSDL_FILE_LOCAL_LOC`

Edit `config.python` or declare environment variables so you can input the ClientID and Client Secret values provided when you registered your application. If you are building a HubExchange application for the Interactive Marketing Hub then, you must also provide the Application Signature (`appsignature` / `FUELSDK_APP_SIGNATURE`).
The `defaultwsdl` / `FUELSDK_DEFAULT_WSDL` configuration must be [changed depending on the Salesforce marketing cloud service](https://code.exacttarget.com/question/there-any-cetificrate-install-our-server-access-et-api "Salesforce Marketing Cloud Forum").
The `baseapiurl` / `FUELSDK_BASE_API_URL` refers to the hostname where the API is hosted, if omitted it will default to [https://www.exacttargetapis.com](https://www.exacttargetapis.com).
The `authenticationurl` / `FUELSDK_AUTH_URL` must also be [changed depending on service](https://code.exacttarget.com/question/not-able-create-accesstoken-when-clientidsecret-associated-preproduction-account "Salesforce Marketing Cloud Forum"). If omitted it will default to [https://auth.exacttargetapis.com/v1/requestToken?legacy=1](https://auth.exacttargetapis.com/v1/requestToken?legacy=1).
The `soapendpoint` / `FUELSDK_SOAP_ENDPOINT` refers to the endpoint that will be used for doing SOAP calls. If omitted it will default to [https://webservice.exacttarget.com/Service.asmx](https://webservice.exacttarget.com/Service.asmx).
The `wsdl_file_local_loc` / `FUELSDK_WSDL_FILE_LOCAL_LOC` allows you to specify the full path/filename where the WSDL file will be located on disk, if for instance you are connecting to different endpoints from the same server.

If you have not registered your application or you need to lookup your Application Key or Application Signature values, please go to App Center at [Code@: Salesforce Marketing Cloud's Developer Community](https://developer.salesforce.com/docs/?filter_text=&service=Marketing%20Cloud "Code@ App Center").


| Environment | WSDL (default) | URL (auth) |
| ----------- | -------------- | ---------- |
| Production  | https://webservice.exacttarget.com/etframework.wsdl | https://auth.exacttargetapis.com/v1/requestToken?legacy=1 |
| Sandbox     | https://webservice.test.exacttarget.com/Service.asmx?wsdl | https://auth-test.exacttargetapis.com/v1/requestToken?legacy=1 |


## Example Request

### Code

All Salesforce marketing cloud objects exposed through the Fuel SDK begin with be prefixed with "ET\_".  Start by working with the ET_List object:

```python
# Add a require statement to reference the Fuel SDK's functionality:
import FuelSDK

# Next, create an instance of the ET_Client class:
myClient = FuelSDK.ET_Client()

# Create an instance of the object type we want to work with:
list = FuelSDK.ET_List()

# Associate the ET_Client to the object using the auth_stub property:
list.auth_stub = myClient

# Utilize one of the ET_List methods:
response = list.get()

# Print out the results for viewing
print 'Post Status: ' + str(response.status)
print 'Code: ' + str(response.code)
print 'Message: ' + str(response.message)
print 'Result Count: ' + str(len(response.results))
print 'Results: ' + str(response.results)
```


### Example Output

```
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
```

## ET\_Client Class

The ET\_Client class takes care of many of the required steps when accessing Salesforce Marketing Cloud's API, including retrieving appropriate access tokens, handling token state for managing refresh, and determining the appropriate endpoints for API requests.  In order to leverage the advantages this class provides, use a single instance of this class for an entire session.  Do not instantiate a new ET_Client object for each request made.

## Responses

All methods on Fuel SDK objects return a generic object that follows the same structure, regardless of the type of call.  This object contains a common set of properties used to display details about the request.

| Parameter | Description                                                     |
| --------- | --------------------------------------------------------------- |
| status    | Boolean value that indicates if the call was successful         |
| code      | HTTP Error Code (will always be 200 for SOAP requests)          |
| message   | Text values containing more details in the event of an Error    |
| results   | Collection containing the details unique to the method called.  |

Get Methods also return an addition value to indicate if more information is available (that information can be retrieved using the getMoreResults method):

 - moreResults - Boolean value that indicates on Get requests if more data is available.


## Samples

Find more sample files that illustrate using all of the available functions for Salesforce Marketing Cloud objects exposed through the API in the objsamples directory.

Sample List:

* [BounceEvent](https://github.com/salesforce-marketingcloud/FuelSDK-Python/tree/master/objsamples/sample_bounceevent.py)
* [Campaign](https://github.com/salesforce-marketingcloud/FuelSDK-Python/tree/master/objsamples/sample_campaign.py)
* [ClickEvent](https://github.com/salesforce-marketingcloud/FuelSDK-Python/tree/master/objsamples/sample_clickevent.py)
* [ContentArea](https://github.com/salesforce-marketingcloud/FuelSDK-Python/tree/master/objsamples/sample_contentarea.py)
* [DataExtension](https://github.com/salesforce-marketingcloud/FuelSDK-Python/tree/master/objsamples/sample_dataextension.py)
* [Email](https://github.com/salesforce-marketingcloud/FuelSDK-Python/tree/master/objsamples/sample_email.py)
* [List](https://github.com/salesforce-marketingcloud/FuelSDK-Python/tree/master/objsamples/sample_list.py)
* [List > Subscriber](https://github.com/salesforce-marketingcloud/FuelSDK-Python/tree/master/objsamples/sample_list_subscriber.py)
* [OpenEvent](https://github.com/salesforce-marketingcloud/FuelSDK-Python/tree/master/objsamples/sample_openevent.py)
* [SentEvent](https://github.com/salesforce-marketingcloud/FuelSDK-Python/tree/master/objsamples/sample_sentevent.py)
* [Subscriber](https://github.com/salesforce-marketingcloud/FuelSDK-Python/tree/master/objsamples/sample_subscriber.py)
* [TriggeredSend](https://github.com/salesforce-marketingcloud/FuelSDK-Python/tree/master/objsamples/sample_triggeredsend.py)
* [UnsubEvent](https://github.com/salesforce-marketingcloud/FuelSDK-Python/tree/master/objsamples/sample_unsubevent.py)


You can also download a copy of wsdl file from the obsamples directory and mention its path in the config file (config.python) like below:  
> wsdl_file_local_loc: /path/to/wsdl/ExactTargetWSDL.xml

Using this wsdl file also resolves [issue:81](https://github.com/salesforce-marketingcloud/FuelSDK-Python/issues/81)

## Development on FuelSDK-Python

If you would like to help contribute to the FuelSDK-Python project, checkout the code from the [GitHub project page](https://github.com/salesforce-marketingcloud/FuelSDK-Python). The use of [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/) is highly recommended. After installing virtualenvwrapper you can run the following commands to setup a sandbox for development.

```
git clone git@github.com:salesforce-marketingcloud/FuelSDK-Python.git
mkvirtualenv FuelSDK-Python
cd FuelSDK-Python
pip install -r requirements.txt
```

You will then have a sandbox which includes all dependencies for doing development on FuelSDK-Python.  
Also you may need to setup your PYTHONPATH environment variable to the cloned root directory so that you can access them from anywhere.  
On Mac/Linux:  
> export PYTHONPATH=$PYTHONPATH:/path/to/FuelSDK-Python

On Windows:  
> set PYTHONPATH=%PYTHONPATH%;C:\path\to\FuelSDK-Python


## Requirements

Python 3.3.x

Libraries:

* pyjwt
* requests
* suds

### Custom Suds Changes (Deprecated)

**Note**: Suds is now patched at runtime when importing the FuelSDK. You no longer need to edit the library. Please be aware of the change.

The default Suds 0.4 Package that is available for download needs to have a couple small fixes applied in order for it to fully support the Fuel SDK. Please update your suds installation using the following instructions:
Suds-jurko 0.6 supports Python 3.x.x

- Download the suds package source from https://pypi.python.org/pypi/suds-jurko/0.6
- Open the file located wihin the uncompressed files at: `suds\mx\appender.py`
- At line 223, the following lines will be present:
```python
child.setText(p.get())
parent.append(child)
for item in p.items():
  cont = Content(tag=item[0], value=item[1])
  Appender.append(self, child, cont)
```

- Replace those lines with:
```python
child_value = p.get()
if(child_value is None):
  pass
else:
  child.setText(child_value)
  parent.append(child)
  for item in p.items():
    cont = Content(tag=item[0], value=item[1])
    Appender.append(self, child, cont)
```

- Open the file located wihin the uncompressed files at `suds\bindings\document.py`
- After line 62 which reads:
```python
n += 1
```

- Add the following lines:
```python
if value is None:
  continue
```
- Install Suds by running the command
```
python setup.py install
``

## Copyright and license
Copyright (c) 2017 Salesforce

Licensed under the MIT License (the "License"); you may not use this work except in compliance with the License. You may obtain a copy of the License in the COPYING file.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
