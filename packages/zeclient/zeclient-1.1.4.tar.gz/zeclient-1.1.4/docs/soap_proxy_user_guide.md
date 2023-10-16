# ZE Python SOAP Proxy User's Guide

## SoapClient class

SoapProxy utilizes *zeep* web services python module to convert method calls to SOAP requests. The parameter of each method is a JSON object and each element in the object maps to the xml element in the SOAP requests. The SoapClient class wraps all the methods for the common use cases. The constructor of the class takes four parameters

1. The WSDL URL
2. The name of the user
3. The password
4. The client name
  
```python
from zeclient.soap_client import SoapClient
import zeclient.soap_util as util
  
wsdl = "http://host.company.com/datadirect/services/dd?wsdl";
proxy = SoapProxy(wsdl, 'user.name', 'password', 'Client')
```

## Methods

* execute_profile()

  The method executes a profile and returns the profile data.
  
  ```python
  result = proxy.execute_profile({'profileOwner': 'user.name',
                                  'profileGroup': 'profile group', 
                                  'profileName': 'profile name'
                                 })
  util.print_profile_result(result)
  ```
* execute_report_query()

  The method retrieves data for a specific report.
  
  For Analytic result
  
  ```python
  result = proxy.execute_report_query('Time Series', {'useDisplayName': 'false',
                                                       'dataRequest': 
                                                                  {'options': {'dataOptions': {'precision': '5'},
                                                                   'timelineOptions': {'startDate': '06/11/2018',
                                                                                       'endDate': '06/15/2018',
                                                                                       'interval': 'Daily'}
                                                                  }
                                                        ,'dataSeries': [{'dataSource': 'Foreign Exchange',
                                                                        'dataReport': 'BANK_CANADA_EXCH_RATES_ALL',
                                                                        'observation': 'FACTOR',
                                                                        'attributes': [{'columnName': 'SRC_UNIT',
                                                                                        'values': ['USD']},
                                                                                       {'columnName': 'TGT_UNIT',
                                                                                        'values': ['CAD']}]
                                                                        }]
                                                       }})
  util.print_profile_result(result)
  ```
  
  For Data Sheet result

  ```python
  result = proxy.execute_report_query('Data Sheet', {'useDisplayName': 'false',
                                                      'dataRequest': 
                                                       {'options': {'dataOptions': {'precision': '5'},
                                                                    'timelineOptions': {'startDate': '06/11/2018',
                                                                                       'endDate': '06/15/2018',
                                                                                       'interval': 'Daily'}
                                                                   }
                                                        ,'dataSeries': [{'dataSource': 'Foreign Exchange',
                                                                        'dataReport': 'BANK_CANADA_EXCH_RATES_ALL',
                                                                        'observation': 'FACTOR',
                                                                        'attributes': [{'columnName': 'SRC_UNIT',
                                                                                        'values': ['USD']},
                                                                                       {'columnName': 'TGT_UNIT',
                                                                                        'values': ['CAD', 'JPY']}]
                                                                        }]
                                                       }})
  
  util.print_profile_result(result)
  ```
* find_curves()

  The method retrieves a list of curves according to the search criteria.
  
  Find curves by properties
  
  ```python
  result = proxy.find_curves({'properties': [{'label': 'Commodity', 'value': 'Gas'}, 
                                              {'label': 'Hub', 'value': 'NBPG'}]})
  util.print_curve_bean(result)
  ```
  
  Find curves by names

  ```python
  result = proxy.find_curves({'names': ['name1', 'name2'],
                               'namesStringMatchType': 'CONTAINS'})
  util.print_curve_bean(result)
  ```
  
* get_forward_curve_data()

  The method retrieves forward curve data for specified curves in a date range.
  
  ```python
  result = proxy.get_forward_curve_data({'curveNames': ['test web service curve 123z'],
                                          'startDate': '2016-09-02',
                                          'endDate': '2016-09-02',
                                          'includePropertiesInResponse': 'false',
                                          'updatedOnly': 'false'})
  util.print_forward_curve_data(result)
  ```
  
* get_time_series_curve_data()

  The method retrieves time series curve data for specified curves in a date range.
  
  ```python
  result = proxy.get_time_series_curve_data({'curveNames': ['tm - hourly'],
                                              'startDate': '2019-01-03',
                                              'endDate': '2019-01-03',
                                              'groupBy': 'Curve Name', # or 'Effective Date'
                                              'includePropertiesInResponse': 'false',
                                              'updatedOnly': 'false'})
  util.print_time_series_curve_data(result)
  ```

