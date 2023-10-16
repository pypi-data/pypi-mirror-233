# ZE Python ZEMA Client User's Guide for SSO (OAuth2)

For OAuth2 authentication, the following four fields for the "auth" parameter are required:

1. idp_type - the type of IDP (only support 3 IdPs for now: ADFS, Okta and Ping Federate). Available options:
    * adfs
    * okta
    * ping
2. idp_url - the IDP URL
3. oauth2_flow - OAuth2 flow type (either OAuth2Flow.ResourceOwnerPasswordCredentialsGrantType or OAuth2Flow.AuthorizationCodeGrantType). Note: ResourceOwnerPasswordCredentialsGrantType is recommended. 
4. domain - the domain name (optional for Ping Federate)

**_Note_**: in case of using Okta or Ping Federate, **Client ID** and **Client Secret** might be needed for Resource Owner Password Credential flow.

## ADFS
### Resource Owner Password Credential flow
```python
auth = {
  'idp_type': 'adfs', 
  'idp_url': 'https://adfs.company.com', 
  'oauth2_flow': OAuth2Flow.ResourceOwnerPasswordCredentialsGrantType,
  'domain': 'company.com'
}
client = ZemaClient(datadirect_url, 'user.name', 'password', 'Client', auth = auth)
```
### Authorization Code flow
```python
auth = {
  'idp_type': 'adfs', 
  'idp_url': 'https://adfs.company.com', 
  'oauth2_flow': OAuth2Flow.AuthorizationCodeGrantType,
  'domain': 'company.com'
}
client = ZemaClient(datadirect_url, 'user.name', 'password', 'Client', auth = auth)
```
## Okta
**Note**: the _**idp_url**_ should be the Authorization Server url configured in Okta.

### Resource Owner Password Credential flow
With the current implementation of Okta (Feb 2021), Client ID and Client Secret are required for ROPC flow.
```python
auth = {
  'idp_type': 'okta', 
  'idp_url': 'https://domain.okta.com/oauth2/default', 
  'oauth2_flow': OAuth2Flow.ResourceOwnerPasswordCredentialsGrantType,
  'idp_client_id': 'the_oauth2_client_id',
  'idp_client_secret': 'secret',
  'domain': 'company.com'
}
```
### Authorization Code flow
```python
auth = {
  'idp_type': 'okta', 
  'idp_url': 'https://domain.okta.com/oauth2/default', 
  'oauth2_flow': OAuth2Flow.AuthorizationCodeGrantType,
  'domain': 'company.com'
}
```

## Ping Federate
### Resource Owner Password Credential flow
Depend on how this OAuth2 client is configured in Ping Federate, ipd_client_id and idp_client_secret will be needed if "CLIENT AUTHENTICATION" is set to "CLIENT SECRET". Please contact your Ping Federate administrator.
```python
auth = {
  'idp_type': 'ping', 
  'idp_url': 'https://ping.company.com:9031', 
  'oauth2_flow': OAuth2Flow.ResourceOwnerPasswordCredentialsGrantType,
  'idp_client_id': 'the_oauth2_client_id',
  'idp_client_secret': 'secret'
}
client = ZemaClient(datadirect_url, 'user.name', 'password', 'Client', auth = auth)
```
### Authorization Code flow
```python
auth = {
  'idp_type': 'ping', 
  'idp_url': 'https://ping.company.com:9031', 
  'oauth2_flow': OAuth2Flow.AuthorizationCodeGrantType
}
client = ZemaClient(datadirect_url, 'user.name', 'password', 'Client', auth = auth)
```