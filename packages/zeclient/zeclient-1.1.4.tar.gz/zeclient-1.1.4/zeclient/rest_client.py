"""
Created on May 3, 2019

@copyright: ZE
@precondition: ZEMA license
@version: 1.0.3
@author: ZE
"""

import json
import pandas as pd
import datetime
import calendar

from zeclient.zema_auth import ZemaAuth


class RestClient:
    """
    A client for ZE REST services
    """

    def __init__(self, url, username, password, client_id, enable_debug=False, proxies=None, auth=None):
        if url.endswith('/'):
            url = url[:-1]

        if url.find('/api') < 0:
            url = url + '/api'

        if url.find('/v1') < 0:
            url = url + '/v1'

        self.__zema_auth = ZemaAuth(url, username, password, client_id, enable_debug, proxies, auth)
        self.__httpclient = None

    def get_report(self, data_source, report, start_date, end_date, select=None, filters=None):
        uri = '/data/sources/{}/reports/{}'.format(data_source, report)

        response = self.__get_httpclient().get_resource(uri, self.__payload(start_date, end_date, select, filters))
        result = self.__data(response)

        d = []
        for e in result:
            for columns in e['columns']:
                o = {}
                o['date'] = e['date']
                for c in columns:
                    o[c['name']] = c['value']
                d.append(o)

        return pd.DataFrame.from_dict(d)

    def get_result_set(self, data_source, report, filters=None):
        uri = "/resultset/sources/{}/reports/{}".format(data_source, report)        
        response = self.__get_httpclient().get_resource(uri, self.__payload(filters=filters))
        json_object = json.loads(response.text)
        series = json_object['data']['series']
        d = []
        for e in series:
            o = {}
            for c in e['column']:
                o[c['name']] = c['value']

            o['minDate'] = e['minDate']
            o['maxDate'] = e['maxDate']
            d.append(o)

        return pd.DataFrame.from_dict(d)

    def find_data_sources(self):
        uri = "/metadata/sources"
        return self.__find(uri)

    def find_reports(self, data_source):
        uri = "/metadata/sources/{}/reports".format(data_source)
        return self.__find(uri)

    def find_report_observations(self, data_source, report):
        uri = "/metadata/sources/{}/reports/{}/observations".format(data_source, report)
        return self.__find(uri)

    def find_report_attributes(self, data_source, report):
        uri = "/metadata/sources/{}/reports/{}/attributes".format(data_source, report)
        return self.__find(uri)

    def find_profile_users(self, user_name=None):
        uri = "/profile/users"
        if user_name is not None:
            uri = uri + "/" + user_name
        return self.__find(uri)

    def find_profile_groups(self, user_name, group_name=None):
        uri = "/profile/users/{}/groups".format(user_name)
        if group_name is not None:
            uri = uri + "/" + group_name
        return self.__find(uri)

    def find_profiles(self, user_name, group_name):
        if group_name is None:
            group_name = "NOGROUP"
        uri = "/profile/users/{}/groups/{}/profiles".format(user_name, group_name)
        return self.__find(uri)

    def find_linked_profiles(self, user_name, group_name, template_name):
        if group_name is None:
            group_name = "NOGROUP"
        uri = "/profile/users/{}/groups/{}/profiles/{}/configs".format(user_name, group_name, template_name)
        return self.__find(uri)

    def find_curve_groups(self, group_name=None):
        uri = "/curve/groups"
        if group_name is not None:
            uri = uri + "/" + group_name
        return self.__find(uri)

    def find_curves(self, group_name, curve_name=None):
        if group_name is None:
            group_name = 'NOGROUP'
        uri = "/curve/groups/{}/curves".format(group_name)
        if curve_name is not None:
            uri = uri + "/" + curve_name
        return self.__find(uri)

    def get_curve_validation(self, curve_group, curve_name, start_date, end_date):
        uri = "/curve/validation/groups/{}/curves/{}".format(curve_group, curve_name)
        response = self.__get_httpclient().get_resource(uri, self.__payload(start_date, end_date))
        return pd.DataFrame.from_dict(self.__data(response))

    def get_curve_group_validation(self, curve_group, start_date, end_date):
        uri = "/curve/validation/groups/{}".format(curve_group)
        response = self.__get_httpclient().get_resource(uri, self.__payload(start_date, end_date))
        return pd.DataFrame.from_dict(self.__data(response))

    def get_batch_status(self, start_date, end_date, batch_name):
        uri = "/curve/batch_status/batches/{}".format(batch_name)
        response = self.__get_httpclient().get_resource(uri, self.__payload(start_date, end_date))
        return pd.DataFrame.from_dict(self.__data(response))

    def get_batch_statuses(self, start_date, end_date, batch_type=None, batch_status=None):
        uri = "/curve/batch_status/batches"
        filters = {}
        if batch_type is not None:
            filters['type'] = batch_type
        if batch_status is not None:
            filters['status'] = batch_status

        response = self.__get_httpclient().get_resource(uri, self.__payload(start_date, end_date, None, filters))
        return pd.DataFrame.from_dict(self.__data(response))

    def get_profile(self, user_name, group_name, profile_name, config_name=None, eff_date=None, start_date=None,
                    end_date=None):
        if group_name is None:
            group_name = "NOGROUP"
        uri = "/profile/data/users/{}/groups/{}/profiles/{}".format(user_name, group_name, profile_name)
        if config_name is not None:
            uri = uri + "/configs/" + config_name

        response = self.__get_httpclient().get_resource(uri, self.__payload(start_date, end_date, None, None, eff_date))
        return pd.DataFrame.from_dict(self.__data(response))

    def get_curve(self, group_name, curve_name, start_date, end_date):
        if group_name is None:
            group_name = "NOGROUP"
        uri = "/curve/data/groups/{}/curves/{}".format(group_name, curve_name)
        response = self.__get_httpclient().get_resource(uri, self.__payload(start_date, end_date))
        return pd.DataFrame.from_dict(self.__data(response))

    def get_curves_in_group(self, group_name, start_date, end_date):
        if group_name is None:
            group_name = "NOGROUP"
        uri = "/curve/data/groups/{}".format(group_name)
        response = self.__get_httpclient().get_resource(uri, self.__payload(start_date, end_date))
        return pd.DataFrame.from_dict(self.__data(response))

    def get_timeseries_curve(self, start_date, end_date, filters=None, include_properties=None):
        return self.__curve_data("Time Series", start_date, end_date, filters, include_properties)

    def get_forward_curve(self, start_date, end_date, filters=None, include_properties=None):
        return self.__curve_data("Futures", start_date, end_date, filters, include_properties)

    def get_options_curve(self, start_date, end_date, filters=None, include_properties=None):
        return self.__curve_data("Options", start_date, end_date, filters, include_properties)

    def upload_curve_data(self, group_name, curve_name, payload, partial_update=None):
        if group_name is None:
            group_name = "NOGROUP"
        uri = "/curve/data/groups/{}/curves/{}".format(group_name, curve_name)
        if partial_update:
            response = self.__get_httpclient().patch_resource(uri, json.dumps(self.__upload_payload(payload)))
        else:
            response = self.__get_httpclient().put_resource(uri, json.dumps(self.__upload_payload(payload)))
        return self.__data(response)

    def enable_debug(self):
        if self.__httpclient is not None:
            self.__httpclient.enable_debug()

    def disable_debug(self):
        if self.__httpclient is not None:
            self.__httpclient.disable_debug()

    def close(self):
        if self.__httpclient is not None:
            self.__httpclient.get_resource('/logout')
            self.__httpclient.close()
        
    def __get_httpclient(self):
        if self.__httpclient is None:
            self.__httpclient = self.__zema_auth.authenticate()
        
        return self.__httpclient

    def __curve_data(self, curve_type, start_date, end_date, filters, include_properties):
        queries = {}
        queries['dataType'] = curve_type
        if include_properties is not None:
            if type(include_properties) == list:
                if len(include_properties) > 0:
                    queries['includeProperties'] = ",".join(include_properties)
            else:
                queries['includeProperties'] = include_properties

        if filters is not None:
            queries['filter'] = self.__curve_filter_query(filters)

        uri = "/curve/data"
        response = self.__get_httpclient().get_resource(uri, self.__payload(start_date, end_date, None, queries))
        return pd.DataFrame.from_dict(self.__data(response))

    def __payload(self, start_date=None, end_date=None, select=None, filters=None, effDate=None):
        payload = {}
        if start_date is not None:
            payload['startDate'] = str(start_date.isoformat())

        if end_date is not None:
            payload['endDate'] = str(end_date.isoformat())

        if select is not None:
            if type(select) == list:
                payload['$select'] = ",".join(select)
            else:
                payload['$select'] = select

        if filters is not None:
            for key in filters:
                t = type(filters[key])
                if t == datetime.date or t == datetime.datetime:
                    payload[key] = str(filters[key].isoformat())
                elif t == bool:
                    payload[key] = str(filters[key]).lower()
                else:
                    payload[key] = filters[key]

        if effDate is not None:
            payload['effectiveDate'] = str(effDate.isoformat())

        return payload

    def __upload_payload(self, payload):
        if payload['effectiveDate'] is not None:
            if isinstance(payload['effectiveDate'], datetime.date):
                payload['effectiveDate'] = str(payload['effectiveDate'].isoformat())

        if payload['data'] is not None:
            for data in payload['data']:
                if isinstance(data["date"], datetime.date):
                    data['date'] = str(data['date'].isoformat())
                if 'value' in data and data['value'] is not None:
                    if isinstance(data['value'], datetime.date) or isinstance(data['value'], datetime.datetime):
                        data['value'] = calendar.timegm(data['value'].timetuple()) * 1000

        return payload

    def __find(self, uri):
        response = self.__get_httpclient().get_resource(uri)
        json_object = json.loads(response.text)
        if type(json_object['data']) != list:
            return pd.DataFrame.from_dict([json_object['data']])
        else:
            return pd.DataFrame.from_dict(json_object['data'])

    def __data(self, response):
        json_object = json.loads(response.text)
        if 'data' not in json_object['data']:
            return json_object['data']
        else:
            return json_object['data']['data']

    def __curve_filter_query(self, curve_filters):
        filters = []
        for key in curve_filters:
            if key == 'properties':
                property_filters = []
                for p in curve_filters['properties']:
                    p_objects = []
                    for k in p:
                        p_objects.append(self.__single_filter(k, p[k]))
                    property_filters.append('{' + ','.join(p_objects) + '}')
                filters.append(key + ':[' + ','.join(property_filters) + ']')
            else:
                filters.append(self.__single_filter(key, curve_filters[key]))

        return '{' + ','.join(filters) + '}'

    def __single_filter(self, key, values):
        filter_clause = key + ":"

        if type(values) == list:
            quoted_values = []
            filter_clause = filter_clause + '['
            for v in values:
                quoted_values.append('"' + v + '"')
            filter_clause = filter_clause + ','.join(quoted_values) + ']'
        else:
            filter_clause = filter_clause + '"' + values + '"'

        return filter_clause
