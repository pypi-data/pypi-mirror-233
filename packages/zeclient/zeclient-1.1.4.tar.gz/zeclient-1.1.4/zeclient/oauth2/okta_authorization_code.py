import json
from urllib.parse import parse_qs, urlparse

import requests


class OktaAuthorizationCode:
    def __init__(self, ze_http_client, dd_url, okta_issuer_url, username, password, verify_ssl=True,
                 proxies=None) -> None:
        self.dd_authorize_url = dd_url + "/oauth2/authorize"
        self.ze_http_client = ze_http_client
        self.verify_ssl = verify_ssl
        self.username = username
        self.password = password
        self.proxies = proxies

        # get the okta hostname?
        url = urlparse(okta_issuer_url)
        if url.scheme is not None and url.netloc is not None:
            self.okta_hostname_url = url.scheme + '://' + url.hostname
        else:
            raise ValueError('Invalid URL: ' + okta_issuer_url)

        self.okta_authentication_url = self.okta_hostname_url + '/api/v1/authn'

    def authenticate(self):

        payload = {
            'username': self.username,
            'password': self.password
        }

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = self.ze_http_client.post(self.okta_authentication_url, data=json.dumps(payload),
                                            proxies=self.ze_http_client.proxies,
                                            headers=headers)

        # get sessionToken
        session_token = response.json()['sessionToken']
        if session_token is None:
            raise ValueError('Invalid session token')

        # Get authorization code
        auth_init = self.ze_http_client.get(self.dd_authorize_url)
        auth_url = auth_init.url + f"&sessionToken={session_token}"
        code = self.ze_http_client.get(auth_url)
