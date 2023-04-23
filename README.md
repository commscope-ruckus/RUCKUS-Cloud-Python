# RUCKUS-Cloud-Python
Python scripts examples for RUCKUS Cloud

- Client Example v200104, Move APs and Toogle .11k & .11r use a deprecated API with API-KEY and cookies for authentication.
- JWT has examples with a new API using JSON Web Tokens for authentication

# JWT Examples
- rcExamplesJWT uses the module rcAPI.py to import several API calls using JWT.
It fetches the tenantId and the JWT, then retrieves the tenant details and changes the 802.11k setting for all networks.

- rcAPI.py contains several API calls using JWT. It includes a function to detect if an API call is async, and if so, it uses the requestId to check the API call execution status.
This module needs to be modified to allow management of delegated accounts. You need to add a new request header to the API calls with a key named x-rks-tenantid, and the value as the tenantId of the delegated account. The function getVenues includes the additional header. See more examples in the RUCKUS-Cloud-Postman repository.
