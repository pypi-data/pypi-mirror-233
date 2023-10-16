'''
ZE SOAP Web Services Clinet

Created on May 21, 2019

@copyright: ZE
@precondition: ZEMA Data Direct license
@version: 1.0.3
@author: ZE
'''

import datetime
from zeclient.soap_proxy import SoapProxy
import zeclient.soap_util as util

class SoapClient:
    '''
    A client for ZE SOAP services
    '''
    def __init__(self,url,username,password,client_id,enable_debug=False,proxies=None):
        if url.endswith('/'):
            url = url[:-1]

        if url.find('/services/dd') < 0:
            url = url + '/services/dd'
                        
        if url.find('?wsdl') < 0:
            url = url + '?wsdl'

        self.wsdl = url        
        self.proxy = SoapProxy(url, username, password, client_id,proxies)
        self.debug = enable_debug
        
        if enable_debug:
            print('SOAP authenticating ' + username + " against " + url)

    def get_profile(self, username, group, name, config=None, effective_date=None):
        param = {}
        param['profileOwner'] = username
        param['profileGroup'] = group
        param['profileName'] = name
        if config is not None:
            param['configName'] = config
            
        if effective_date is not None:
            param['effectiveDate'] = effective_date.isoformat()
        
        result = self.proxy.execute_profile(param)
        return util.profile_result_to_df(result)
    
    def get_report(self, datasource, report, start_date, end_date, observations=None, filters=None):
        if not observations: # get all observations if it's empty
            lvs = self.proxy.retrieve_observations(datasource, report)
            observations = []
            for e in lvs:
                observations.append(e.value)
            
        dr = {}
        dr['options'] = {'dataOptions': {'precision': '5'},
                         'timelineOptions': {'startDate': self.__date_to_string(start_date),
                                             'endDate': self.__date_to_string(end_date)}
                        }
        dataseries = {'dataSource': datasource,
                      'dataReport': report,
                      'observation': observations.pop()
                     }
            
        attr = []
        if filters is not None:
            for key in filters:
                afilter = {'columnName': key}
                values = []
                t = type(filters[key])
                if t == datetime.date or t == datetime.datetime:
                    values.append(str(filters[key].isoformat()))
                elif t == bool:
                    values.append(str(filters[key]).lower())
                elif t == list:
                    values = filters[key]
                else:
                    values.append(filters[key])
                afilter['values'] = values
                attr.append(afilter)
        
        if attr:
            dataseries['attributes'] = attr
        
        dr['dataSeries'] = dataseries
        
        if observations:
            olist = []
            for o in observations:
                olist.append({'observation': o})
            dr['observations'] = olist
        
        if self.debug:
            print(dr)
            
        result = self.proxy.execute_report_query('Data Sheet', {'useDisplayName': 'false',
                                                                'dataRequest': dr})

        return util.profile_result_to_df(result, True)

    def find_curves(self, filters):
        g_filters =  filters['groups'] if 'groups' in filters else {}
        n_filters = filters['names'] if 'names' in filters else {}
        p_filters = filters['properties'] if 'properties' in filters else {}

        param = {}

        if g_filters:
            for op in g_filters:
                param['groupsStringMatchType'] = self.__get_string_match(op)
                t = type(g_filters[op])
                if t == list:
                    param['groups'] = g_filters[op]
                else:
                    param['groups'] = [g_filters[op]]
        
        if n_filters:
            for op in n_filters:
                param['namesStringMatchType'] = self.__get_string_match(op)
                t = type(n_filters[op])
                if t == list:
                    param['names'] = n_filters[op]
                else:
                    param['names'] = [n_filters[op]]
        
        if p_filters:
            properties = []
            for n in p_filters:
                properties.append({'label': n, 'value': p_filters[n]})
            param['properties'] = properties
        
        param['includeProperties'] = filters['includeProperties'] if 'includeProperties' in filters else False
        param['includeObservations'] = filters['includeObservations'] if 'includeObservations' in filters else False
        
        result = self.proxy.find_curves(param)

        return util.curve_bean_to_df(result)
            
    def get_forward_curve(self, start_date, end_date, name = None, property_filters = None):
        param = self.__get_curve_data_request(start_date, end_date, name, property_filters)
        
        result = self.proxy.get_forward_curve_data(param)
        
        return util.forward_curve_to_df(result)
    
    def get_timeseries_curve(self, start_date, end_date, name = None, property_filters = None):
        param = self.__get_curve_data_request(start_date, end_date, name, property_filters)
        
        result = self.proxy.get_time_series_curve_data(param)
        
        return util.time_series_curve_to_df(result)
    
    def get_options_curve(self, start_date, end_date, name = None, property_filters = None):
        param = self.__get_curve_data_request(start_date, end_date, name, property_filters)
        param['pivoted'] = False
        
        result = self.proxy.get_options_curve_data(param)
        
        return util.options_curve_to_df(result)
    
    def insert_update_curve_data(self, data):
        result = self.proxy.insert_update_curve_data(data)
        return util.insert_update_curve_data_result_to_df(result)
    
    def __date_to_string(self, d):
        return d.strftime("%m/%d/%Y")
    
    def __get_string_match(self, op):
        m = ''
        if op == 'startswith':
            m = 'STARTS_WITH'
        elif op == 'endswith':
            m = 'ENDS_WITH'
        elif op == 'equals':
            m = 'EQUALS'
        elif op == 'contains':
            m = 'CONTAIINS'
        else:
            raise Exception('Unknow match type - {}'.format(op))
        return m

    def __get_curve_data_request(self, start_date, end_date, name = None, property_filters = None):
        param = {}
        
        if name is not None:
            if type(name) == list:
                param['curveNames'] = name
            else:
                param['curveNames'] = [name]
            
        param['startDate'] = start_date.isoformat()
        param['endDate'] = end_date.isoformat()
        
        if property_filters is not None:
            properties = []
            for p in property_filters:
                vs = property_filters(p)
                t = type(vs)
                if t == list:
                    for v in vs:
                        properties.append({'label': p, 'value': v})
                else:
                    properties.append({'label': p, 'value': vs})
        
        param['includePropertiesInResponse'] = False
        param['updatedOnly'] = False
        param['pivoted'] = False

        return param
    
