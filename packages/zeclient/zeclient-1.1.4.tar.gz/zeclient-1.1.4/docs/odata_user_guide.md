# ZE Python OData Client User's Guide

## ODataClient class

To utilize ZE Python OData Client, an instance of ODataClient class needs to be created. The constructor of the class takes four parameters

1. The URL of ZEMA Data Direct server
2. The name of the user who has ZEMA OData license
3. The password
4. The client name
  
```python
from zeclient.odata_client import ODataClient
  
datadirect_url = "http://host.company.com/datadirect";
client = ODataClient(datadirect_url, 'user.name', 'password', 'Client')
```

## Entities and Columns

Here is a list of entities and columns that are accessible by the client methods. All columns can be used in the *filters* parameter of the methods mentioned below.

|Entity|Columns|Description|
| ---- | ----- | --------- |
|data_sources|name, display_name, description, url|a list of data sources|
|reports|source, name, display_name, granularity, gmt_offset, commodity, data_entity_id|a list of data reports|
|report_data____nnnnn|unknown|a specific report data entity and different report data entities have different columns|
|profile_users|name, first_name, last_name, group, email|a list of profile owners|
|profile_groups|user, name|a list of profile groups|
|profiles|user, group, name, version, is_template, data_entity_id|a list of profiles|
|linked_profiles|user, template_group, template, group, name, version, data_entity_id| a list of linked profiles|
|profile_data____nnnnn|unknown|a specific profile data entity and different profile data entities have different columns|
|curve_groups|name|a list of curve groups|
|curves|user, group, name|a list of curves|
|futures_curve_data|name,opr_date, contract_start, contract_end, contract_code, contract_year, type, value, date_modified|forward curve data|
|time_series_curve_data|name,opr_date, opr_hour, opr_minute, type, value, date_modified|time series curve data|

## Common Method Parameters

There are three common parameters used by all the methods.
* select

  The "select" parameter specifies a list of columns to select.
  ```python
  select = ['name', 'opr_date', 'type', 'value']
  ```
* filters

  The "filters" parameter is used to filter data based on the specified column values. The parameter is an JSON object. A basic filter contains three elements.
  ```
  {'column_name': {'op': 'operator', 'value': ['column value 1', 'column value 2']}}
  ```
  The operator can be 'eq', 'ge', 'gt', 'le', 'lt', 'contains', 'startswith', 'endswith'. Note that the last three are only for string values.
  
  Here is a sample filter
  ```python
  filters = {'name': {'op': 'contains', 'value': 'NYMEX'},
             'ticker': {'op': 'eq', 'value': ['OB', 'OD']},
             'opr_date': [{'op': 'ge', 'value': date(2019-05-01)}, {'op': 'ge', 'value': date(2019-05-02)}],
             'contract_year': {'op': 'ge', 'value': 2020}}
  ```
* top

  The "top" parameter specified the number of records to return
  ```python
  top = 10
  ```

## Method Return

All methods return a pandas' DataFrame.
```
               name    opr_date   type    value
0  daily curve name  2016-08-24  CLOSE  123.4
1  daily curve name  2016-08-25  CLOSE  123.5
2  daily curve name  2016-08-26  CLOSE  123.6
```

## Methods

* get_profile(username, group, name, config=None, select=None, filters=None, top=None, order_by=None, skip=None, effective_date=None)

  The method retrieves data for a specified profile.
  
  Get data for a profile.
  ```python
  result = client.get_profile('user.name', 'profile group', 'profile name')
  ```
  
  Get data for a linked profile.
  ```python
  result = client.get_profile('user.name', 'template group', 'template name', 'config name')
  ```
  
  Add some filters
  ```python
  filters = {'opr_hour': {'op': 'ge', 'value': 20},
             'b' : {'op': 'ge', 'value': 10}}
  result = client.get_profile('user.name', 'profile group', 'profile name', filters = filters, top=100)
  ```
  
* get_report(datasource, report, select=None, filters=None, top=None, order_by=None)

  This method retrieves data for a specified report.
  
  Get data for a report in a date range.
  ```python
  filters = {'opr_date': [{'op': 'ge', 'value': date(2019, 5, 1)}, {'op': 'le', 'value': date(2019, 5, 31)}]}
  result = client.get_report('NYMEX', 'NYMEX_FUTURES_SETTLEMENT', filters = filters)
  
  ```
  
  Select columns and add more filters.
  ```python
  select = ['opr_date', 'ticker', 'contract_month', 'contract_year', 'settle']
  filters = {'opr_date': [{'op': 'ge', 'value': date(2019, 5, 1)}, {'op': 'le', 'value': date(2019, 5, 31)}],
             'ticker': {'op': 'eq', 'value': ['OB', 'OD']}
  result = client.get_report('NYMEX', 'NYMEX_FUTURES_SETTLEMENT', select = select, filters = filters)
  
  ```

* get_forward_curve(name=None, select=None, filters=None, top=None)

  The method retrieves data for forward curves.

  Get data for a curve in a date range.
  ```python
  filters = {'opr_date': {'op': 'eq', 'value': date(2019, 5, 1)}}
  name = 'my curve'
  result = client.get_forward_curve(name, filters = filters)
  ```
  
  Select columns and add more filters.
  ```python
  select = ['name', 'opr_date', 'type', 'contract_year', 'contract_code', 'value']
  filters = {'opr_date': {'op': 'eq', 'value': date(2019, 5, 1)}}
  name = ['my curve 1', 'my curve 2']
  result = client.get_forward_curve(name, select = select, filters = filters, top=100)
  ```
    
* get_timeseries_curve(name=None, select=None, filters=None, top=None)

  The method retrieves data for time series curves.

  Get data for a curve in a date range.
  ```python
  select = ['name', 'opr_date', 'opr_hour', 'type', 'value']
  filters = {'opr_date': {'op': 'eq', 'value': date(2019, 5, 1)}}
  name = ['my curve 1', 'my curve 2']
  result = client.get_time_series_curve(name, select = select, filters = filters, top=100)
  ```

* get_options_curve(name=None, select=None, filters=None, top=None)

  The method retrieves data for options curves.

  
* find_profile_users(select=None, filters=None, top=None)

  The method retrieves a list of profile owners.
  
  Get all users.
  ```python
  result = client.find_profile_users()
  ```

  Get filtered users.  
  ```python
  filters= {'name': {'op': 'startswith', 'value': 'prefix'}}
  result = client.find_profile_users(filters = filters)
  ```
    
* find_profile_groups(select=None, filters=None, top=None)

  The method retrieves a list of profile groups.
  
  Get all profile groups.
  ```python
  result = client.find_profile_groups()
  ```

  Get filtered groups.
  ```python
  filters= {'name': {'op': 'contains', 'value': 'nymex'}}
  result = client.find_profile_groups(filters = filters)
  ```

* find_profiles(select=None, filters=None, top=None)

  The method retrieves a list of profiles.
  
  Get all profiles.
  ```python
  result = client.find_profileps()
  ```

  Get filtered profiles for a list of users.
  ```python
  select = ['user', 'group', 'name', 'data_entity_id']
  filters= {'user': {'op': 'eq', 'value': ['user1', 'user2']},
            'name': {'op': 'contains', 'value': 'nymex'}}
  result = client.find_profiless(select = select, filters = filters)
  ```

* find_linked_profiles(select=None, filters=None, top=None)

  The method retrieves a list of linked profiles.
  
  Get all linked profiles.
  ```python
  result = client.find_linked_profileps()
  ```

  Get filtered linked profiles for a list of users.
  ```python
  filters= {'user': {'op': 'eq', 'value': ['user1', 'user2']},
            'name': {'op': 'contains', 'value': 'nymex'}}
  result = client.find_linked_profiless(filters = filters)
  ```
    
* find_data_sources(select=None, filters=None, top=None)

  The method retrieves a list of data sources.
  
  Get all data sources.
  ```python
  result = client.find_data_sources()
  ```

  Get filtered data sources.
  ```python
  filters= {'name': {'op': 'contains', 'value': 'NYMEX'}}
  result = client.find_data_sources(filters = filters)
  ```

* find_reports(select=None, filters=None, top=None)

  The method retrieves a list of data reports.
  
  Get all data reports.
  ```python
  result = client.find_reports()
  ```

  Get filtered data reports from a list of specified data sources
  ```python
  filters= {'source': {'op': 'eq', 'value':['NYMEX', 'ICE']},
            'name': {'op': 'contains', 'value': 'NYMEX'}}
  result = client.find_data_sources(filters = filters)
  ```
* find_curve_groups(select=None, filters=None, top=None)

  The method retrieves a list of curve groups.
  
  Get all curve groups.
  ```python
  result = client.find_curve_groups()
  ```

  Get filtered curve groups.
  ```python
  filters= {'name': {'op': 'contains', 'value': 'nymex'}}
  result = client.find_curve_groups(filters = filters)
  ```

* find_curves(select=None, filters=None, top=None)

  The method retrieves a list of curves.
  
  Get all curves.
  ```python
  result = client.find_curves()
  ```

  Get filtered curves from a list of specified curve groups.
  ```python
  filters= {'group': {'op': 'eq', 'value': ['group 1', 'group 2']}, 
            'name': {'op': 'contains', 'value': 'keyword'}}
  result = client.find_curves(filters = filters)
  ```
* close()

  Terminating the session.
  
* enable_debug()

  Enabling debug mode.

* disable_debug()

  Disabling debug mode.
