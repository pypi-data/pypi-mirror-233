# ZE Python REST Client User's Guide

## RestClient class

To utilize ZE Python REST Client, an instance of RestClient class needs to be created. The constructor of the class takes four parameters

1. The URL of ZEMA Data Direct server
2. The name of the user who has ZEMA Data Direct license
3. The password
4. The client name
  
```python
from zeclient.rest_client import RestClient
  
datadirect_url = "http://host.company.com/datadirect";
client = RestClient(datadirect_url, 'user.name', 'password', 'Client')
```

## Method Return

All methods return a pandas' DataFrame.
```
     date        type   price
0    2016-08-24  CLOSE  123.4
1    2016-08-25  CLOSE  123.5
2    2016-08-26  CLOSE  123.6
```

## Methods

* get_report(self, data_source, report, start_date, end_date, select=None, filters=None)

  The method retrieves data for a specified report in a date range.

  Get data for a report on a specific date
  ```python
  result = client.get_report('NYMEX', 'NYMEX_FUTURES_SETTLEMENT', date(2019, 5, 1), date(2019, 5, 1))
  ```
  
  Get data for a report in a date range by selecting columns and using filters. The filters can include report columns, 'changedSince' and 'maxRecords'.
  ```python
  select = ['TICKER', 'CONTRACT_YEAR', 'CONTRACT_MONTH', 'PRICE']
  filters = {'TICKER': ['HA','KR'], 
             'CONTRACT_YEAR': 2020, 
             'CONTRACT_MONTH': [1, 2, 3],
             'changedSince': datetime(2010, 5, 14, 14, 20, 30),
             'maxRecords': 10}
  result = client.get_report('NYMEX', 'NYMEX_FUTURES_SETTLEMENT', date(2019, 5, 1), date(2019, 5, 10), select=select, filters=filters)
  ```
  
  Note that a 'date' column is always included in the result.

* get_result_set(data_source, report, filters=None)

  The method retrieves available result sets for a report and the return columns are report columns, 'minDate' and 'maxDate'.
  
  Get all result sets for a report
  ```python
  result = client.get_result_set('NYMEX', 'NYMEX_FUTURES_SETTLEMENT')
  ```
  
  Get filtered result sets. The filters can include report columns, 'changedSince', 'newResultsetOnly' and 'maxRecords'.
  ```python
  filters = {'TICKER': ['HA','KR'], 
             'changedSince': datetime(2010, 5, 14, 14, 20, 30),
             'newResultsetOnly': True,
             'maxRecords': 10}
  result = client.get_result_set('NYMEX', 'NYMEX_FUTURES_SETTLEMENT', filters=filters)
  ```

* find_data_sources()

  The method returns all the available data sources for the user. The columns returned are name, displayName, description and url.
  
* find_reports(data_source)

  The method retrieves all data reports under the specified data source. The columns returned are name, displayName, commodityType, marketType, granularity and gmtOffset.
  
* find_report_observations(data_source, report)

  The method retrieves all observations for a report. The columns returned are name, displayName, numerator, denominator, dataType and marketType.
  
* find_report_attributes(data_source, report)

  The method retrieves all attributes for a report. The columns returned are name, displayName, and dataType.

* find_profile_users()

  The method returns profile users

* find_profile_groups(profile_user)

  The method finds out all profile groups for a specific user

* find_profiles(profile_user, profile_group)

  The method finds out all profiles under a group for a specific user

* find_linked_profiles(profile_user, profile_group, template_name)

  The method finds out all linked profiles (configs) for a template under a group for a specific user

* get_profile(user_name, group_name, profile_name, config_name=None, eff_date=None, start_date=None, end_date=None)

  The method executes a profile and returns the result. Effective date (eff_date), start date and end date are optional.

* find_curve_groups()

  The method returns all curve groups

* find_curves(group_name)

  The method finds out all curves under a group

* get_curve_validation(curve_group, curve_name, start_date, end_date)

  The method returns curve validation status for a curve under a group within a date range

* get_curve_group_validation(curve_group, start_date, end_date)

  The method returns curve validation status for all curves under a group within a date range

* get_batch_status(start_date, end_date, batch_name)

  The method gets the batch status for a batch within a date range

* get_batch_statuses(start_date, end_date, batch_type=None, batch_status=None)

  The method gets the batch statuses for all batche instances that have a specific batch type within a date range

* get_curve(group_name, curve_name, start_date, end_date)

  The method retrieves curve data for a curve under a specific group within a date range

* get_curves_in_group(group_name, start_date, end_date)

  The method retrieves curve data for curves under a specific group within a date range

* get_forward_curve(start_date, end_date, filters=None, include_properties=None)

  The method retrieves futures curve data for filtered curves within a date range

  The filters can include curve groups, batches and curve properties. The result can include curve properties specified in include_properties argument.
  ```python
  filters = {'groups': ['group 1','group 2'], 
             'batches': ['batch 1', 'batch 2'],
             'properties': [{'name': 'property name 1', 'values':['value 11', 'value 12']},
                            {'name': 'property name 2', 'values':['value 21', 'value 22']}]}
  include_properties = ['property name 1']

  result = client.get_forward_curve(date(2020,2, 1), date(2020, 2, 1), filters, include_properties)
  ```
* get_timeseries_curve(start_date, end_date, filters=None, include_properties=None)

  The method retrieves time series curve data for filtered curves within a date range

* get_options_curve(start_date, end_date, filters=None, include_properties=None)

  The method retrieves options curve data for filtered curves within a date range

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

  Logging out and terminating the session.
  
* enable_debug()

  Enabling debug mode.

* disable_debug()

  Disabling debug mode.
  