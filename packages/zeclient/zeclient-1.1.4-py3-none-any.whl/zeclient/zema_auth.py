from zeclient.http_client import ZeHttpClient
from zeclient.oauth2.generic_resource_owner_password_flow import GenericResourceOwnerPasswordFlow
from zeclient.oauth2.adfs_authorization_code import AdfsAuthorizationCode
from zeclient.oauth2.oauth2_flow import OAuth2Flow
from http.client import HTTPConnection
import logging

from zeclient.oauth2.okta_authorization_code import OktaAuthorizationCode
from zeclient.oauth2.ping_authorization_code import PingAuthorizationCode


class ZemaAuth:

    def __init__(self, url, username, password, client_id, enable_debug=False, proxies=None, auth=None) -> None:
        self.auth_url = url.replace('/odata4', '/odata')
        self.url = url
        self.username = username
        self.password = password
        self.client_id = client_id
        self.enable_debug = enable_debug
        self.proxies = proxies
        self.auth = auth
        self.verify_ssl = True
        self.logger = logging.getLogger(self.__module__)
        if self.auth is not None:
            self.verify_ssl = self.auth['verify_ssl'] if 'verify_ssl' in self.auth else True
            self.idp = self.auth['idp_type'] if 'idp_type' in self.auth else None
            self.idp_url = self.auth['idp_url'] if 'idp_url' in self.auth else None
            self.idp_token_url = self.auth['idp_token_url'] if 'idp_token_url' in self.auth else None
            self.idp_client_id = self.auth['idp_client_id'] if 'idp_client_id' in self.auth else None
            self.idp_client_secret = self.auth['idp_client_secret'] if 'idp_client_secret' in self.auth else None
            self.oauth2_flow = self.auth['oauth2_flow'] if 'oauth2_flow' in self.auth else None
            self.domain = self.auth['domain'] if 'domain' in self.auth else None
            if self.domain is not None:
                self.username = self.username + '@' + self.domain
        if self.enable_debug:
            HTTPConnection.debuglevel = 1

    def authenticate(self):

        self.enable_debug and self.logger.debug('Authenticating ' + self.username + " against " + self.auth_url)

        httpclient = None

        if self.auth is not None and self.oauth2_flow is not None:
            self.enable_debug and self.logger.debug(f'Authenticating using the provided oauth2_flow: {self.oauth2_flow}')
            if self.oauth2_flow is OAuth2Flow.ResourceOwnerPasswordCredentialsGrantType:
                resource_owner_flow = GenericResourceOwnerPasswordFlow(self.username,
                                                                       self.password,
                                                                       verify_ssl=self.verify_ssl,
                                                                       proxies=self.proxies,
                                                                       auth=self.auth)
                headers = {
                        'Authorization': f'Bearer {resource_owner_flow.get_bearer_token()}'
                }
                httpclient = ZeHttpClient(self.url, self.proxies, headers=headers, verify_ssl=self.verify_ssl)

            elif self.oauth2_flow is OAuth2Flow.AuthorizationCodeGrantType:                
                # ADFS
                if 'adfs' == self.idp:
                    httpclient = ZeHttpClient(self.url, self.proxies, verify_ssl=self.verify_ssl)
                    adfs_authorization_code = AdfsAuthorizationCode(httpclient,
                                                                    dd_url=self.auth_url,
                                                                    username=self.username,
                                                                    password=self.password,
                                                                    verify_ssl=self.verify_ssl)
                    adfs_authorization_code.authenticate()
                # OKTA
                elif 'okta' == self.idp:
                    httpclient = ZeHttpClient(self.url, self.proxies, verify_ssl=self.verify_ssl)
                    okta_authorization_code = OktaAuthorizationCode(httpclient,
                                                                    dd_url=self.auth_url,
                                                                    okta_issuer_url=self.idp_url,
                                                                    username=self.username,
                                                                    password=self.password,
                                                                    verify_ssl=self.verify_ssl)
                    okta_authorization_code.authenticate()
                # Ping Federate
                elif 'ping' == self.idp:
                    httpclient = ZeHttpClient(self.url, self.proxies, verify_ssl=self.verify_ssl)
                    ping_authorization_code = PingAuthorizationCode(httpclient,
                                                                    dd_url=self.auth_url,
                                                                    ping_url=self.idp_url,
                                                                    username=self.username,
                                                                    password=self.password,
                                                                    verify_ssl=self.verify_ssl,
                                                                    proxies=self.proxies)
                    ping_authorization_code.authenticate()
                # Key Cloak
                elif 'keycloak' == self.idp:
                    raise ValueError(f'The selected OAuth2 flow is not supported {self.oauth2_flow} for Keycloak')
                else:
                    raise ValueError(f'The IDP - {self.idp} is currently not supported')
            else:
                raise ValueError(f'The selected OAuth2 flow is not supported {self.oauth2_flow}')
            
        if httpclient is None:
            httpclient = ZeHttpClient(self.url, self.proxies, verify_ssl=self.verify_ssl)
            httpclient.login(self.username, self.password, self.client_id)

        if self.enable_debug:
            httpclient.enable_debug()

        return httpclient
