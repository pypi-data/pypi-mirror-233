# ZE Python ZEMA Client User's Guide

## ZemaClient class

To utilize ZE Python ZEMA Client, an instance of ZemaClient class needs to be created. The constructor of the class takes four mandatory parameters

1. The URL of ZEMA Data Direct server
2. The name of the user who has ZEMA OData license
3. The password
4. The client name
  
and three optional parameters
5. enable_debug - to enable/disable debug (default is False)
6. proxies - to specify HTTP proxies (default is None)
7. auth -  to specify authentication parameters for OAuth2 or disable certificate verification (default is None)

Sample code for simple user name / password authentication
```python
from zeclient.zema_client import ZemaClient
  
datadirect_url = "https://host.company.com/datadirect";
auth = {'verify_ssl': False}
client = ZemaClient(datadirect_url, 'user.name', 'password', 'Client', auth = auth)
```
For OAuth2 authentication, currently only resource owner password flow is supported. The following six fields for the "auth" parameter are required

1. idp_token_url - the token URL
2. idp_client_id - the client id
3. idp_client_secret - the client secret
4. idp_scope - the scope. it should be "openid" in most situations
5. oauth2_flow - OAuth2 flow type (OAuth2Flow.ResourceOwnerPasswordCredentialsGrantType)
6. domain - the domain name 

```python
auth = {
  'idp_token_url': 'https://adfs-uat.zepower.com/adfs/oauth2/token', 
  'idp_client_id': 'client_id_string', 
  'idp_client_secret': 'client_secret_string', 
  'idp_scope': 'openid', 
  'oauth2_flow': OAuth2Flow.ResourceOwnerPasswordCredentialsGrantType,
  'domain': 'company.com'
}
client = ZemaClient(datadirect_url, 'user.name', 'password', 'Client', auth = auth)
```

## Common Method Parameters

There are five parameters that are available for OData based methods.
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

* skip

  The "skip" parameter specified the number of records to skip
  ```python
  skip = 100
  ```

* order_by

  The "order_by" parameter specified a column to be ordered by
  ```python
  order_by = 'opr_date desc'
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

  The method retrieves data for a specified profile and returns the following columns
  * opr_date [,opr_hour, opr_minute], a, b, c, ...
  
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
  
* get_report(datasource, report, select=None, filters=None, top=None, order_by=None, skip=None)

  This method retrieves data for a specified report and returns the following columns
  * The date, attributes and observations of the requested report
  
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

* get_forward_curve(name=None, select=None, filters=None, top=None, order_by=None, skip=None)

  The method retrieves data for forward curves and returns the following columns
  * name, opr_date, contract_start, contract_end, contract_code, contract_year, type, value, date_modified

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

* get_forward_data_and_property(start_date, end_date, curve_filters, include_properties=None, top=None)

  The method retrieves data and properties for forward curves filtered by properties, groups and batches and returns the following columns and additional property columns if include_properties argument is set to 'All' or a list of propoery names. Note that this method is based on ZE REST Web Services so some common parameters are not supported.
  * name, group, opr_date, contract_start, contract_end, contract_code, contract_year, contract_granularity, type, value, date_modified

  Get data for curves with specific properties and values.
  ```python
  curve_filters = {
      'properties':[
          {'name': 'prop name1', 'values': ['prop value1']}, 
          {'name': 'prop name2', 'values': ['prop value2']}
      ]
  }
  result = client.get_forward_data_and_property(date(2019, 5, 1), date(2019, 5, 1), curve_filters, include_properties='All')
  ```
    
* get_timeseries_curve(name=None, select=None, filters=None, top=None, order_by=None, skip=None)

  The method retrieves data for time series curves and returns the following columns
  * name, opr_date, opr_hour, opr_minute, type, value, date_modified

  Get data for a curve in a date range.
  ```python
  select = ['name', 'opr_date', 'opr_hour', 'type', 'value']
  filters = {'opr_date': {'op': 'eq', 'value': date(2019, 5, 1)}}
  name = ['my curve 1', 'my curve 2']
  result = client.get_time_series_curve(name, select = select, filters = filters, top=100)
  ```
  
* get_timeseries_data_and_property(start_date, end_date, curve_filters, include_properties=None, top=None)

  The method retrieves data and properties for time series curves filtered by properties, groups and batches and returns the following columns and additional property columns if include_properties argument is set to 'All' or a list of propoery names. Note that this method is based on ZE REST Web Services so some common parameters are not supported.
  * name, group, opr_date, opr_hour, opr_minute, type, value, date_modified

  Get data and properties for curves filtered by properties and groups.
  ```python
  curve_filters = {
      'groups': ['group1'],
      'properties':[
          {'name': 'prop name1', 'values': ['prop value1']}, 
          {'name': 'prop name2', 'values': ['prop value2']}
      ]
  }
  result = client.get_timeseries_data_and_property(date(2019, 5, 1), date(2019, 5, 1), curve_filters,  include_properties=['prop name1', 'prop name2'])
  ```

* get_options_curve(name=None, select=None, filters=None, top=None, order_by=None, skip=None)

  The method retrieves data for options curves and returns the following columns
  * name, opr_date, contract_start, contract_end, contract_code, contract_year, type, put_call, level_type, level_value, strip_unit, spread_length, contract_month_2, contract_year_2, contract_start_2, contract_end_2, value, date_modified

* get_options_data_and_property(start_date, end_date, curve_filters, include_properties=None, top=None)

  The method retrieves data and properties for options curves filtered by properties, groups and batches and returns the following columns and additional property columns if include_properties argument is set to 'All' or a list of propoery names. Note that this method is based on ZE REST Web Services so some common parameters are not supported.
  * name, group, opr_date, contract_start, contract_end, contract_code, contract_year, type, contract_granularity, put_call, level_type, level_value, strip_unit, spread_length, contract_month_2, contract_year_2, contract_start_2, contract_end_2, value, date_modified

* find_profile_users(select=None, filters=None, top=None)

  The method retrieves a list of profile owners and returns the following columns
  * name, first_name, last_name, group, email
  
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

  The method retrieves a list of profile groups and returns the following columns
  * user, name
  
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

  The method retrieves a list of profiles and returns the following columns
  * user, group, name, version, is_template, data_entity_id
  
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

  The method retrieves a list of linked profiles and returns the following columns
  * user, template_group, template, group, name, version, data_entity_id
  
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

  The method retrieves a list of data sources and returns the following columns
  * name, display_name, description, url
  
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

  The method retrieves a list of data reports and returns the following columns
  * source, name, display_name, granularity, gmt_offset, commodity, data_entity_id
  
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

  The method retrieves a list of curve groups and returns the following column
  * name
  
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

  The method retrieves a list of curves and returns the following columns
  * user, group, name
  
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
  
* find_holiday_groups(select=None, filters=None, top=None)

  The method retrieves a list of holiday groups and returns the following column
  * group_name, group_display_name
  
  Get all holiday groups.
  ```python
  result = client.find_holiday_groups()
  ```

  Get filtered holiday groups.
  ```python
  filters= {'group_name': {'op': 'eq', 'value': 'us_holidays'}}
  result = client.find_holiday_groups(filters = filters)
  ```
  
* get_holidays(select=None, filters=None, top=None, order_by=None, skip=None)

  The method retrieves a list of holidays and returns the following column
  * group_name, group_display_name, holiday_date, description
  
  Get holidays for a specific group in a date range.
  ```python
  filters = {'group_name': {'op': 'eq', 'value': ['us_holidays']},
             'holiday_date': [{'op': 'ge', 'value': date(2022, 1, 1)},
                              {'op': 'le', 'value': date(2022, 12, 31)}]}
  result = client.get_holidays(filters = filters)
  ```

* upload_curve_data(self, group_name, curve_name, payload, partial_update=None)

  The method uploads curve data based on effective date. The payload requires two properties,
  'effective_date', and 'data', where data is a list of curve data objects. If partial_update parameter
  is passed as True, this will create a PATCH request to only update available 'data' records of the effective date.
  If partial_update parameter is not passed, this will call a PUT request to delete and replace all records
  on the given effective_date

  ```python
  payload = {
    "effectiveDate": datetime.date(2023, 1, 15),
    "data": [
      {
        "date": datetime.date(2023, 1, 15),
        "granularity": "value",
        "type": "value",
        "value": "value",
        "comment": "comment"
      },
      {
        "date": datetime.date(2023, 1, 16),
        "granularity": "value",
        "type": "value",
        "value": "value",
        "comment": "comment"
      }
    ]
  }
  
  response = client.upload_curve_data(curve_group, curve_name, payload, partial_update=True)
  ```
  
* close()

  Terminating the session.
  
* enable_debug()

  Enabling debug mode.

* disable_debug()

  Disabling debug mode.
   
