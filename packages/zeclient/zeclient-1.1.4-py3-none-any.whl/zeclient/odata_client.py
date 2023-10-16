"""
Created on May 3, 2019

@copyright: ZE
@precondition: ZEMA OData license
@version: 1.0.3
@author: ZE
"""

import json
import pandas as pd
import urllib
from datetime import date
from datetime import datetime

from zeclient.zema_auth import ZemaAuth


class ODataClient:
    """
    A client for ZE OData services
    """

    def __init__(self, url, username, password, client_id, enable_debug=False, proxies=None, auth=None):
        self.odata_version = 4
        if url.endswith('/'):
            url = url[:-1]

        if url.find('/odata') < 0:
            url = url + '/odata4'

        if url.find('/odata4') < 0:
            raise Exception('ZemaClient only supports OData version 4')

        if url.find('/v1') < 0:
            url = url + '/v1'

        self.__httpclient = None
        self.__zema_auth = ZemaAuth(url, username, password, client_id, enable_debug, proxies, auth)

    def get_profile(self, username, group, name, config=None, select=None, filters=None, top=None, order_by=None,
                    skip=None, effective_date=None):
        profile_id = self.get_profile_entity_id(username, group, name, config)

        payload = self.__payload(select=select, filters=filters, top=top, order_by=order_by, skip=skip,
                                 effective_date=effective_date)

        response = self.__get_httpclient().get_resource('/' + profile_id, payload)

        return pd.DataFrame.from_dict(self.__values(response))

    def get_report(self, datasource, report, select=None, filters=None, top=None, order_by=None, skip=None):
        report_id = self.get_report_entity_id(datasource, report)

        payload = self.__payload(select=select, filters=filters, top=top, order_by=order_by, skip=skip)

        response = self.__get_httpclient().get_resource('/' + report_id, payload)

        return pd.DataFrame.from_dict(self.__values(response))

    def find_profile_users(self, select=None, filters=None, top=None):
        return self.__find('/profile_users', select=select, filters=filters, top=top)

    def find_profile_groups(self, select=None, filters=None, top=None):
        return self.__find('/profile_groups', select=select, filters=filters, top=top)

    def find_profiles(self, select=None, filters=None, top=None):
        return self.__find('/profiles', select=select, filters=filters, top=top)

    def find_linked_profiles(self, select=None, filters=None, top=None):
        return self.__find('/linked_profiles', select=select, filters=filters, top=top)

    def find_data_sources(self, select=None, filters=None, top=None):
        return self.__find('/data_sources', select=select, filters=filters, top=top)

    def find_reports(self, select=None, filters=None, top=None):
        return self.__find('/reports', select=select, filters=filters, top=top)

    def find_holiday_groups(self, select=None, filters=None, top=None):
        return self.__find('/holiday_groups', select=select, filters=filters, top=top)

    def get_holidays(self, select=None, filters=None, top=None, order_by=None, skip=None):
        payload = self.__payload(select=select, filters=filters, top=top, order_by=order_by, skip=skip)
        response = self.__get_httpclient().get_resource('/holidays', payload)
        return pd.DataFrame.from_dict(self.__values(response))

    def find_curve_groups(self, select=None, filters=None, top=None):
        return self.__find('/curve_groups', select=select, filters=filters, top=top)

    def find_curves(self, select=None, filters=None, top=None):
        return self.__find('/curves', select=select, filters=filters, top=top)

    def get_forward_curve(self, name=None, select=None, filters=None, top=None, order_by=None, skip=None):
        return self.__curve_data('/futures_curve_data', name, select, filters, top, order_by, skip)

    def get_timeseries_curve(self, name=None, select=None, filters=None, top=None, order_by=None, skip=None):
        return self.__curve_data('/time_series_curve_data', name, select, filters, top, order_by, skip)

    def get_options_curve(self, name=None, select=None, filters=None, top=None, order_by=None, skip=None):
        return self.__curve_data('/options_curve_data', name, select, filters, top, order_by, skip)

    def get_profile_entity_id(self, username, group, name, config=None):
        uri = None
        if group is None or group == '':
            group = 'NOGROUP'

        if config is None or config == '':
            uri = "/profiles(user='{}',group='{}',name='{}')".format(username, group, name)
        else:
            uri = "/linked_profiles(user='{}',template_group='{}',template='{}',name='{}')".format(username, group,
                                                                                                   name, config)
        
        response = self.__get_httpclient().get_resource(uri, {'$format': 'json'})
        json_object = json.loads(response.text)
        profile_id = None

        if 'd' not in json_object:  # odata 4
            profile_id = json_object['data_entity_id']
        else:
            profile_id = json_object['d']['data_entity_id']

        return profile_id

    def get_report_entity_id(self, datasource, report):
        uri = "/reports(source='{}',name='{}')".format(datasource, report)
        response = self.__get_httpclient().get_resource(uri, {'$format': 'json'})
        json_object = json.loads(response.text)
        report_id = None

        if 'd' not in json_object:  # odata 4
            report_id = json_object['data_entity_id']
        else:
            report_id = json_object['d']['data_entity_id']

        return report_id

    def enable_debug(self):
        if self.__httpclient is not None:
            self.__httpclient.enable_debug()

    def disable_debug(self):
        if self.__httpclient is not None:
            self.__httpclient.disable_debug()

    def close(self):
        if self.__httpclient is not None:
            self.__httpclient.close()
        
    def __get_httpclient(self):
        if self.__httpclient is None:
            self.__httpclient = self.__zema_auth.authenticate()
            
        return self.__httpclient

    def __find(self, entity_url, select=None, filters=None, top=None):
        payload = self.__payload(select=select, filters=filters, top=top)
        response = self.__get_httpclient().get_resource(entity_url, payload)
        return pd.DataFrame.from_dict(self.__values(response))

    def __curve_data(self, uri, name=None, select=None, filters=None, top=None, order_by=None, skip=None):
        if name is not None:
            if filters is None:
                filters = {}
            filters['name'] = {'op': 'eq', 'value': name}

        payload = self.__payload(select=select, filters=filters, top=top, order_by=order_by, skip=skip)
        response = self.__get_httpclient().get_resource(uri, payload)

        return pd.DataFrame.from_dict(self.__values(response))

    def __values(self, response):
        values = None
        json_object = json.loads(response.text)
        if self.odata_version == 4:
            values = json_object['value']
        else:
            values = json_object['d']['results']
            for e in values:
                del e['__metadata']

        return values

    def __payload(self, select=None, filters=None, top=None, order_by=None, skip=None, effective_date=None):
        payload = {'$format': 'json'}
        if select is not None:
            payload["$select"] = ",".join(select) if type(select) == list else select

        filter_clause = None

        if filters is not None:
            all_columns = []
            for key in filters:
                afilter = filters[key]
                if type(afilter) == list:
                    for e in afilter:
                        self.__filter(all_columns, key, e)
                else:
                    self.__filter(all_columns, key, afilter)

            filter_clause = ('' if filter_clause is None else (filter_clause + ' and ')) + " and ".join(all_columns)

        if filter_clause is not None:
            payload["$filter"] = filter_clause.encode(encoding='utf-8')

        if top is not None:
            payload["$top"] = top

        if order_by is not None:
            payload["$orderby"] = order_by

        if skip is not None:
            payload["$skip"] = skip

        if effective_date is not None:
            if isinstance(effective_date, date):
                payload["effective_date"] = str(effective_date.isoformat())
            elif isinstance(effective_date, str):
                payload["effective_date"] = effective_date

        # by default, requests encode space to plus and this is incorrect
        payload = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)

        return payload

    def __filter(self, all_expressions, name, operation):
        if type(operation['value']) == list:
            expressions = []
            for e in operation['value']:
                expressions.append(self.__single_filter(name, {'op': operation['op'], 'value': e}))

            all_expressions.append('(' + ' or '.join(expressions) + ')')
        else:
            all_expressions.append(self.__single_filter(name, operation))

        return all_expressions

    def __single_filter(self, name, operation):
        e = operation['value']

        if len(operation['op']) > 2:
            if operation['op'] == 'startswith':
                return "startswith({},'{}') eq true".format(name, e)
            elif operation['op'] == 'endswith':
                return "endswith({},'{}') eq true".format(name, e)
            elif operation['op'] == 'contains':
                return "indexof({},'{}') ge 0".format(name, e)
            else:
                raise Exception('Unknown operator - ' + operation['op'])
        else:
            if type(e) == str:
                return name + ' ' + operation['op'] + ' ' + "'" + e + "'"
            elif type(e) == date:
                return name + ' ' + operation['op'] + ' ' + str(e.isoformat())
            elif type(e) == datetime:
                return name + ' ' + operation['op'] + ' ' + str(e.isoformat()) + 'Z' if e.tzinfo is None else ''
            else:
                return name + ' ' + operation['op'] + ' ' + str(e)
