"""
Created on May 8, 2019

@copyright: ZE
@precondition: ZEMA OData license
@version: 1.0.3
@author: ZE
"""

import requests
import json
import logging

class ZeHttpClient:
    """
    A Http client that interacts with ZE's REST and OData services
    """

    def __init__(self, url, proxies=None, headers=None, verify_ssl=True):
        self.url = url
        self.debug = False
        self.session = requests.Session()
        self.is_odata = True
        self.odata_version = -1
        if url.find('/api/v1') > 0:
            self.is_odata = False

        self.proxies = proxies
        self.headers = headers
        self.verify_ssl = verify_ssl
        self.logger = logging.getLogger(self.__module__)

    def enable_debug(self):
        self.debug = True

    def disable_debug(self):
        self.debug = False

    def login(self, username, password, client_id):
        if self.is_odata:
            self.session.auth = (username + '@' + client_id, password)
            response = self.session.get(self.url, proxies=self.proxies, verify=self.verify_ssl)
            if response.status_code != 200:
                raise Exception(
                    'Could not login. Http Code: {}, Message: {}'.format(response.status_code, response.text))
        else:
            response = self.session.post(self.url + '/login',
                                         data={'username': username, 'password': password, 'client': client_id},
                                         proxies=self.proxies, verify=self.verify_ssl)
            if response.status_code != 200:
                raise Exception(
                    'Could not login. Http Code: {}, Message: {}'.format(response.status_code, response.text))

            text = json.loads(response.text)
            if text['status'] != 'SUCCESS':
                raise Exception('Could not login. Message: {}'.format(text['message']))

    def get_resource(self, uri, payload=None):
        return self.get(self.url + uri, payload)

    def get(self, url, payload=None):
        response = self.session.get(url, params=payload, proxies=self.proxies, headers=self.headers,
                                    verify=self.verify_ssl)
        self.__check_response(response)
        if self.debug and self.logger.isEnabledFor(logging.DEBUG):
            self.__print_response(response)
        return response

    def post_resource(self, uri, payload):
        return self.post(self.url + uri, data=payload, proxies=self.proxies, headers=self.headers,
                         verify=self.verify_ssl)

    def post(self, url, data, proxies=None, headers=None, verify=True):
        response = self.session.post(url, data=data, proxies=proxies, headers=headers,
                                     verify=verify)
        self.__check_response(response)
        if self.debug and self.logger.isEnabledFor(logging.DEBUG):
            self.__print_response(response)
        return response

    def put_resource(self, uri, payload):
        return self.put(self.url + uri, data=payload, proxies=self.proxies, headers=self.headers,
                        verify=self.verify_ssl)

    def put(self, url, data, proxies=None, headers=None, verify=True):
        response = self.session.put(url, data=data, proxies=proxies, headers=headers,
                                    verify=verify)
        self.__check_response(response)
        if self.debug and self.logger.isEnabledFor(logging.DEBUG):
            self.__print_response(response)
        return response

    def patch_resource(self, uri, payload):
        return self.patch(self.url + uri, data=payload, proxies=self.proxies, headers=self.headers,
                          verify=self.verify_ssl)

    def patch(self, url, data, proxies=None, headers=None, verify=True):
        response = self.session.patch(url, data=data, proxies=proxies, headers=headers,
                                      verify=verify)
        self.__check_response(response)
        if self.debug and self.logger.isEnabledFor(logging.DEBUG):
            self.__print_response(response)
        return response

    def close(self):
        self.session.close()

    def __print_response(self, response):
        self.logger.debug('Request URL => {}'.format(response.url))
        self.logger.debug('Response Code => {}'.format(response.status_code))
        # may fail with encoding
        try:
            self.logger.debug('Response => {}'.format(response.text))
        except:
            self.logger.debug('Response => {...}')

    def __check_response(self, response):
        if response.status_code > 299:
            raise Exception(
                'Error encountered. Http Code: {}, Message: {}, Url: {}'.format(response.status_code, response.text,
                                                                                response.url))
