# ZE Python Client

The ZE Python Client provides a unified module - ZemaClient for retrieving data from ZEMA web services.

## Prerequisites

Python 3.5 or above and the following packages

 * requests
 * lxml
 * pandas
 * zeep
 * dicttoxml
 
The packages will be automatically installed during the installation.
 
## Installation

```
pip install zeclient
```

## Usage
 
```python
  from zeclient.zema_client import ZemaClient
    
  # ZEMA Data Direct server URL
  datadirect_url = "http://host.company.com/datadirect";
    
  # Create ZEMA client instance and start a session
  client = ZemaClient(datadirect_url, 'user.name', 'password', 'Client')
    
  # Get profile data
  result = client.get_profile('user.name', 'profile group', 'profile name')
```

## Support
Please report bugs to support@ze.com
