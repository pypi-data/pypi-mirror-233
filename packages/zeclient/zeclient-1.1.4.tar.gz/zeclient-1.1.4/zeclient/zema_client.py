"""
ZE ZEMA Clinet

Created on May 28, 2019

@copyright: ZE
@precondition: ZEMA Data Direct license
@version: 1.0.3
@author: ZE
"""

from zeclient.odata_client import ODataClient
from zeclient.rest_client import RestClient

class ZemaClient:

    def __init__(self, datadirect_url, username, password, client_id, enable_debug=False, proxies=None, auth=None):
        self.odata_client = ODataClient(datadirect_url, username, password, client_id, enable_debug, proxies=proxies,
                                        auth=auth)
        self.rest_client = RestClient(datadirect_url, username, password, client_id, enable_debug, proxies=proxies,
                                      auth=auth)

    def get_profile(self, username, group, name, config=None, select=None, filters=None, top=None, order_by=None,
                    skip=None, effective_date=None):
        return self.odata_client.get_profile(username, group, name, config, select, filters, top, order_by, skip,
                                             effective_date)

    def get_report(self, datasource, report, select=None, filters=None, top=None, order_by=None, skip=None):
        return self.odata_client.get_report(datasource, report, select, filters, top, order_by, skip)

    def get_holidays(self, select=None, filters=None, top=None, order_by=None, skip=None):
        return self.odata_client.get_holidays(select, filters, top, order_by, skip)

    def find_profile_users(self, select=None, filters=None, top=None):
        return self.odata_client.find_profile_users(select, filters, top)

    def find_profile_groups(self, select=None, filters=None, top=None):
        return self.odata_client.find_profile_groups(select, filters, top)

    def find_profiles(self, select=None, filters=None, top=None):
        return self.odata_client.find_profiles(select, filters, top)
    
    def find_holiday_groups(self, select=None, filters=None, top=None):
        return self.odata_client.find_holiday_groups(select, filters, top)

    def find_linked_profiles(self, select=None, filters=None, top=None):
        return self.odata_client.find_linked_profiles(select, filters, top)

    def find_data_sources(self, select=None, filters=None, top=None):
        return self.odata_client.find_data_sources(select, filters, top)

    def find_reports(self, select=None, filters=None, top=None):
        return self.odata_client.find_reports(select, filters, top)

    def find_curve_groups(self, select=None, filters=None, top=None):
        return self.odata_client.find_curve_groups(select, filters, top)

    def find_curves(self, select=None, filters=None, top=None):
        return self.odata_client.find_curves(select, filters, top)

    def get_forward_curve(self, name=None, select=None, filters=None, top=None, order_by=None, skip=None):
        return self.odata_client.get_forward_curve(name, select, filters, top, order_by, skip)

    def get_timeseries_curve(self, name=None, select=None, filters=None, top=None, order_by=None, skip=None):
        return self.odata_client.get_timeseries_curve(name, select, filters, top, order_by, skip)

    def get_options_curve(self, name=None, select=None, filters=None, top=None, order_by=None, skip=None):
        return self.odata_client.get_options_curve(name, select, filters, top, order_by, skip)

    def get_forward_data_and_property(self, start_date, end_date, curve_filters, include_properties=None, top=None):
        column_map = {"name": "name",
                      "oprDate": "opr_date",
                      "contractMonth": "contract_month",
                      "contractYear": "contract_year",
                      "contractStart": "contract_start",
                      "contractEnd": "contract_end",
                      "type": "type",
                      "value": "value",
                      "dateModified": "date_modified",
                      "group": "group",
                      "contractGranularity": "contract_granularity"}
        pd = self.rest_client.get_forward_curve(start_date, end_date, curve_filters, include_properties)
        pd = pd.rename(columns=column_map)
        if top is not None:
            return pd.head(top)
        else:
            return pd

    def get_timeseries_data_and_property(self, start_date, end_date, curve_filters, include_properties=None, top=None):
        column_map = {"name": "name",
                      "oprDate": "opr_date",
                      "oprHour": "opr_hour",
                      "oprMinute": "opr_minute",
                      "type": "type",
                      "value": "value",
                      "group": "group",
                      "dateModified": "date_modified"}
        pd = self.rest_client.get_timeseries_curve(start_date, end_date, curve_filters, include_properties)
        pd = pd.rename(columns=column_map)
        if top is not None:
            return pd.head(top)
        else:
            return pd

    def get_options_data_and_property(self, start_date, end_date, curve_filters, include_properties=None, top=None):
        column_map = {'name': 'name',
                      'group': 'group',
                      'oprDate': 'opr_date',
                      'contractMonth': 'contract_code',
                      'contractYear': 'contract_year',
                      'contractStart': 'contract_start',
                      'contractEnd': 'contract_end',
                      'levelType': 'level_type',
                      'levelValue': 'level_value',
                      'putCall': 'call_put',
                      'spreadLength': 'spread_length',
                      'stripUnit': 'strip_unit',
                      'type': 'type',
                      'contractMonth2': 'contract_month_2',
                      'contractYear2': 'contract_year_2',
                      'contractStart2': 'contract_start_2',
                      'contractEnd2': 'contract_end_2',
                      'contractGranularity': 'contract_granularity',
                      'value': 'value',
                      'dateModified': 'date_modified'}
        pd = self.rest_client.get_options_curve(start_date, end_date, curve_filters, include_properties)
        pd = pd.rename(columns=column_map)
        if top is not None:
            return pd.head(top)
        else:
            return pd

    def upload_curve_data(self, group_name, curve_name, payload, partial_update=None):
        return self.rest_client.upload_curve_data(group_name, curve_name, payload, partial_update)

    def enable_debug(self):
        self.odata_client.enable_debug()
        self.rest_client.enable_debug()

    def disable_debug(self):
        self.odata_client.disable_debug()
        self.rest_client.disable_debug()

    def close(self):
        self.odata_client.close()
        self.rest_client.close()
