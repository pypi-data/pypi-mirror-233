# ZE Python SOAP Client User's Guide

## SoapClient class

SoapClient utilizes SoapProxy module which is built on *zeep* web services python module to convert method calls to SOAP requests. The SoapClient class wraps all the methods for the common use cases. The constructor of the class takes four parameters

1. The Data Direct server URL
2. The name of the user
3. The password
4. The client name
  
```python
from zeclient.soap_client import SoapClient
  
datadirect_url = "http://host.company.com/datadirect";
client = SoapClient(datadirect_url, 'user.name', 'password', 'Client')
```

## Method Return

All methods return a pandas' DataFrame.

## Methods

* get_profile(username, group, name, config=None, effective_date=None)

  The method executes a profile (analytic or linked analytic) and returns the profile data.
  
  ```python
  result = client.get_profile('user.name', 'profile group', 'profile name')
  ```
  
  Get data for a linked analytic
  
    ```python
  result = client.get_profile('user.name', 'profile group', 'template name', config='linked anlytic name')
  ```
  
  Specify an effective date
  
    ```python
  result = client.get_profile('user.name', 'profile group', 'profile name', effective_date = date(2019, 5, 1))
  ```
  
  Sample data
  ```
             Date  Hour  Minute      a       b
    0  2019-05-01     1       0  1.141   2.141
    1  2019-05-01     2       0  1.141   3.141
    2  2019-05-01     3       0  1.141   4.141
  ```
* get_report(datasource, report, start_date, end_date, observations=None, filters=None)

  The method retrieves data for a specific report.
  
  Get all observations for a report
  ```python
  result = client.get_report('CME', 'CME_NYMEX_OPTIONS', date(2019, 5, 1), date(2019, 5, 2))
  ```
  
  Get all selected observations for a report and apply attribute filters
  ```python
  result = client.get_report('CME', 'CME_NYMEX_OPTIONS', date(2019, 5, 1), date(2019, 5, 2), observations = ['PX', 'SZ'], filters = {'TICKER': 'BA', 'CONTRACT_YEAR': [2020, 2021]})
  ```
  
  Sample data
  ```
           Date       Commodity Type  Ticker  Contract Month Contract Year  Volume     Price
    0  2019-05-01  Crude Oil Markets      BA               1          2020  789230  14.00000
    1  2019-05-01  Crude Oil Markets      BA               2          2020  892032  14.00000
    2  2019-05-01  Crude Oil Markets      BA               3          2020  289934  13.99000
  ```

* find_curves(filters)

  The method retrieves a list of curves according to the filters applied. There are three filters - 'names', 'groups' and 'properties'. The 'names' and 'groups' filters use four matching types - 'startswith', 'endswith', 'contains' and 'equals'.
  
  Find curves by names and properties
  
  ```python
  result = client.find_curves({'properties': {'Commodity': 'Gas'}, 
                                              {'Hub': 'NBPG'},
                               'names': {'contains': ['cme', 'nymex']}})
  ```
  
  Find curves by groups

  ```python
  result = client.find_curves({'groups': {'equals': 'abc'}})
  ```
  
  Sample data
  ```
        user       group           name      id        class
    0   1560  group name   curve name 1   39683      Futures
    1   1560  group name   curve name 2   39684      Futures
    2   1560  group name   curve name 3   39685  Time Series
  ```
  
* get_forward_curve(start_date, end_date, name = None, property_filters = None)

  The method retrieves forward curve data for specified curves in a date range. The 'property_filters' is used to filter out curves by curve properties.
  
  Get data by name
  ```python
  result = client.get_forward_curve(date(2019, 5, 1), date(2019, 5, 1), 'curve name')
  ```

  Get data by property filters
  ```python
  result = client.get_forward_curve(date(2019, 5, 1), date(2019, 5, 1), property_filters = {'Commodity': 'Gas'},  {'Hub': 'NBPG'})
  ```
  
  Sample data
  ```
        name    opr_date contract_start contract_end contract_code contract_year   type value          date_modified
    0  name1  2019-05-01     2019-09-01   2019-09-30             9          2019 SETTLE  1.23 2019-09-30 9:27:30.062
  ```
  
* get_timeseries_curve(start_date, end_date, name = None, property_filters = None)

  The method retrieves time series curve data for specified curves in a date range.
  
  ```python
  client.get_timeseries_curve(date(2019, 5, 1), date(2019, 5, 31), name = ['name 1', 'name 2'])
  ```
  
  Sample data
  ```
        name    opr_date opr_hour opr_minute   type value          date_modified
    0  name1  2019-05-01        3          0 CLOSE   1.23 2019-09-30 9:27:30.062
  ```

* get_options_curve(start_date, end_date, name = None, property_filters = None)

  The method retrieves options curve data for specified curves in a date range.
  
  ```python
  client.get_options_curve(date(2019, 5, 1), date(2019, 5, 31), name = ['name 1', 'name 2'])
  ```
  
  Sample data
  ```
        name    opr_date contract_start contract_end contract_code contract_year   type put_call   level_type level_value strip_unit spread_length contract_start_2 contract_end_2 contract_month_2 contract_year_2 value          date_modified
    0  name1  2019-05-01     2019-09-01   2019-09-30             9          2019 SETTLE     Call Strike Price         3.9        N/A             0       1010-01-01     1010-01-01               -1              -1  1.23 2019-09-30 9:27:30.062
  ```
