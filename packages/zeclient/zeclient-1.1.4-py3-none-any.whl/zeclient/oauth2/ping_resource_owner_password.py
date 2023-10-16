import base64
import json
from urllib.parse import parse_qs, urlparse

import requests
from bs4 import BeautifulSoup


class PingResourceOwnerPassword:
    def __init__(self, ze_http_client, dd_url, ping_url, username, password, idp_client_id, idp_client_secret,
                 verify_ssl=True, proxies=None) -> None:
        self.dd_authorize_url = dd_url + "/oauth2/authorize"
        self.ze_http_client = ze_http_client
        self.verify_ssl = verify_ssl
        self.username = username
        self.password = password
        self.proxies = proxies
        self.ping_token_url = ping_url + "/as/token.oauth2"
        self.idp_client_id = idp_client_id
        self.idp_client_secret = idp_client_secret

    def authenticate(self):
        code = f'{self.idp_client_id}:{self.idp_client_secret}'
        encoded = base64.b64encode(code.encode('ascii')).decode('ascii')

        headers = {
            'authorization': f'Basic {encoded}',
            'content-type': 'application/x-www-form-urlencoded'
        }

        payload = {'username': self.username,
                   'password': self.password,
                   'grant_type': 'password',
                   'scope': 'openid'}

        response = self.ze_http_client.post(self.ping_token_url, data=payload, proxies=self.ze_http_client.proxies,
                                            headers=headers, verify=self.verify_ssl)

        tokens = response.json()
        return tokens["access_token"]
