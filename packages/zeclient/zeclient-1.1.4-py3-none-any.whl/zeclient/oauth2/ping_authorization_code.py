import json
from urllib.parse import parse_qs, urlparse

import requests
from bs4 import BeautifulSoup


class PingAuthorizationCode:
    def __init__(self, ze_http_client, dd_url, ping_url, username, password, verify_ssl=True,
                 proxies=None) -> None:
        self.dd_authorize_url = dd_url + "/oauth2/authorize"
        self.ze_http_client = ze_http_client
        self.verify_ssl = verify_ssl
        self.username = username
        self.password = password
        self.proxies = proxies
        self.ping_hostname_url = ping_url

    def authenticate(self):
        # initialize the dd_authorize_url to get more settings of DD
        auth_init = self.ze_http_client.get(self.dd_authorize_url)
        # auth_url = auth_init.url

        doc = BeautifulSoup(auth_init.text, 'html.parser')
        form = doc.find('form')
        action = form.get('action')

        port_url = self.ping_hostname_url + action

        payload = {
            'pf.username': self.username,
            'pf.pass': self.password,
            # 'pf.adapterId': 'HTMLFormAdapter',
        }

        response = self.ze_http_client.post(port_url, data=payload,
                                            proxies=self.proxies, verify=self.verify_ssl)


