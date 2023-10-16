'''
ZE SOAP Web Services Proxy

Created on Jan 03, 2019

@copyright: ZE
@precondition: ZEMA Data Direct license
@version: 1.0.1
@author: ZE
'''

from lxml import etree
from zeep import Plugin
from zeep import Client

from dicttoxml import dicttoxml

class SoapProxy:
    def __init__(self,wsdl,user_name,password,client_id,proxies):
        class ExecuteReportQuery(Plugin):
            def set_xml_data(self, xml_data):
                self.xml_data = xml_data
            def egress(self, envelope, http_headers, operation, binding_options):
                r = envelope.xpath('//executeReportQueryRequest')
                if (r == None or len(r) == 0):
                    return envelope, http_headers
                p=next(r[0].iterancestors())
                p.remove(r[0])
                parser = etree.XMLParser(strip_cdata=False)
                new_request = etree.XML(self.xml_data.encode('utf-8'), parser=parser)
                p.append(new_request)
                xml_string = etree.tostring(envelope)
                parser = etree.XMLParser(strip_cdata=False)
                new_envelope = clean_request_data(etree.XML(xml_string, parser=parser))
                return new_envelope, http_headers
        
        class SendDataRequest(Plugin):
            def set_xml_data(self, xml_data):
                self.xml_data = xml_data
            def egress(self, envelope, http_headers, operation, binding_options):
                r = envelope.xpath('//request')
                if (r == None or len(r) == 0):
                    return envelope, http_headers
                p=next(r[0].iterancestors())
                p.remove(r[0])
                parser = etree.XMLParser(strip_cdata=False)
                new_request = etree.XML(self.xml_data.encode('utf-8'), parser=parser)
                p.append(new_request)
                xml_string = etree.tostring(envelope)
                parser = etree.XMLParser(strip_cdata=False)
                new_envelope = clean_request_data(etree.XML(xml_string, parser=parser))
                return new_envelope, http_headers
            
        self.wsdl=wsdl
        self.plugin = ExecuteReportQuery()
        self.plugin2 = SendDataRequest()
        self.client = Client(wsdl=wsdl, plugins=[self.plugin, self.plugin2])
                 
        self.token=self.client.service.getAccessTokenForAccount(user_name,password,client_id)
        if proxies is not None:
            self.client.transport.session.proxies = proxies

    def get_token(self):
        return self.token
    def execute_profile(self, data):
        pass
    def execute_report_query(self,data_type,data):
        pass
    def find_curves(self,data):
        pass
    def retrieve_curve_data_beans(self,data):
        pass
    def get_forward_curve_data(self,data):
        pass
    def get_time_series_curve_data(self,data):
        pass
    def get_options_curve_data(self,data):
        pass
    def retrieve_observations(self,data):
        pass
    def send_data_request(self,data_type,data,fmt):
        pass
    def insert_update_curve_data(self,data):
        pass
    def close(self):
        pass

def check_token(token):
    assert(token != None), "The proxy object has been detroyed"

def execute_profile(self, data):
    check_token(self.token)
    return self.client.service.executeProfile(self.token,data)

def retrieve_curve_data_beans(self, data):
    check_token(self.token)
    return self.client.service.retrieveCurveDataBeans(self.token,data)

def find_curves(self, data):
    check_token(self.token)
    return self.client.service.findCurves(self.token,data)

def get_forward_curve_data(self, data):
    check_token(self.token)
    return self.client.service.getForwardCurveData(self.token,data)

def get_time_series_curve_data(self, data):
    check_token(self.token)
    return self.client.service.getTimeSeriesCurveData(self.token,data)

def get_options_curve_data(self, data):
    check_token(self.token)
    return self.client.service.getOptionsCurveData(self.token,data)

def retrieve_observations(self, datasource, report):
    check_token(self.token)
    return self.client.service.retrieveObservations(self.token,datasource,report)

def insert_update_curve_data(self, data):
    check_token(self.token)
    return self.client.service.insertUpdateCurveData(self.token,data)

def close(self):
    self.client.service.logout(self.token)
    self.token = None

def execute_report_query(self, data_type, data):
    TIME_SERIES_TYPE="timeSeriesRequest"
    ADVANCED_TYPE="advancedQueryRequest"
    if data_type=='Time Series':
        request_type=TIME_SERIES_TYPE
    elif data_type=='Data Sheet':
        request_type=ADVANCED_TYPE
    else:
        print("Usage: execute_report_query('Time Series' or 'Data Sheet', data)")
        return

    xml_data = dicttoxml(data,attr_type=False,custom_root='executeReportQueryRequest').decode()
    xml_data = xml_data.replace("<dataRequest>",'<dataRequest xmlns:ns6="datarequest.datadirect.ze.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ns6:'+request_type+'">') 
    self.plugin.set_xml_data(xml_data)

    result = self.client.service.executeReportQuery(self.token, {'useDisplayName': '',
                                                   'dataRequest':{}
                                                   })
    return result

def send_data_request(self, data_type, data, fmt):
    TIME_SERIES_TYPE="timeSeriesRequest"
    ADVANCED_TYPE="advancedQueryRequest"
    if data_type=='Time Series':
        request_type=TIME_SERIES_TYPE
    elif data_type=='Data Sheet':
        request_type=ADVANCED_TYPE
    else:
        print("Usage: sendDataRequest('Time Series' or 'Data Sheet', data)")
        return

    xml_data = dicttoxml(data,attr_type=False,custom_root='request').decode()
    xml_data = xml_data.replace("<request>",'<request xmlns:ns6="datarequest.datadirect.ze.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ns6:'+request_type+'">') 
    self.plugin2.set_xml_data(xml_data)

    result = self.client.service.sendDataRequest(self.token, 
                                                 {},
                                                 fmt
                                                )
    return result

def clean_request_data(new_envelope):
    for elem in new_envelope.findall(".//item"):
        parent = elem.find('..')
        if parent is not None:
            elem.tag = parent.tag
            grand = parent.find('..')
            grand.append(elem)
            
    for elem in new_envelope.xpath(".//*[not(node())]"):
        elem.getparent().remove(elem)
        
    return new_envelope

SoapProxy.execute_profile=execute_profile
SoapProxy.retrieve_curve_data_beans=retrieve_curve_data_beans
SoapProxy.find_curves=find_curves
SoapProxy.execute_report_query=execute_report_query
SoapProxy.get_forward_curve_data=get_forward_curve_data
SoapProxy.get_time_series_curve_data=get_time_series_curve_data
SoapProxy.get_options_curve_data=get_options_curve_data
SoapProxy.retrieve_observations=retrieve_observations
SoapProxy.send_data_request = send_data_request
SoapProxy.insert_update_curve_data=insert_update_curve_data
SoapProxy.close=close

