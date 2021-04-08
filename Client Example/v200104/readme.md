# Ruckus Cloud API Client Example
This is a client example using the Ruckus Cloud API.

The API is divided into separate sections:
* Tenant API that manages the authentication, tenant, venues, admins, delegation. Basically anything not related to a specific technology stack.
* Separate APIs for each technology stack: Wifi, Switch (Future), LTE (Future)

The API-classes in this example were generated automatically by [OpenAPI Generator](https://github.com/openapitools/openapi-generator) (packages `ruckus_cloud_tenant` and `ruckus_cloud_wifi`).

#Virtual-Env
The sample includes all required packages in a virtual environment:
* To enable the virtual-env, run `source venv/Scripts/activate`  
Note: For Windows, run `venv\Scripts\activate.bat`
* Alternatively, run `pip3 install -r requirements.txt` to manually install all packages

## Getting started
The main body of the example can be found in `ruckus_cloud.py`.  
Set your credentials and Tenant ID in the `Global params` section there.  

Run `python3 main.py` to start the client.

#Note:
The OpenAPI python client implementation has issues with the `oneof` keyword.  
Specifically, it does not correctly implement the discriminator, resulting in an ``ValueError: Invalid value for `auth_radius_id`, must not be `None` ``
 or similar error when retrieving a Network or NetworkDeep model. 
To resolve, the following changes were made to the generated code:

`ruckus_cloud_wifi/api_client.py`
![diff api_client](diff_api_client.png)

`ruckus_cloud_wifi/model/network.py`
![diff network](diff_network.png)
