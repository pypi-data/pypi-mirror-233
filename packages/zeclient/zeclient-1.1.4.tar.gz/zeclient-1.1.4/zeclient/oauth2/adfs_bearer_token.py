import requests
from urllib.parse import parse_qs, urlparse


class AdfsBearerToken:

    def __init__(self, adfs_hostname_url, dd_url, username, password, verify_ssl=True, proxies=None) -> None:
        adfs_token_url = adfs_hostname_url + "/adfs/oauth2/token"
        adfs_authorize_url = adfs_hostname_url + "/adfs/oauth2/authorize"

        self.dd_authorize_url = dd_url + "/oauth2/authorize"

        # initialize the dd_authorize_url to get more settings of DD
        auth_init = requests.get(self.dd_authorize_url, verify=verify_ssl, proxies=proxies)
        auth_url = auth_init.url
        query = parse_qs(urlparse(auth_url).query)

        if len(query) == 0:
            raise ValueError(f'Could not init the connection to: {auth_url}')

        # Extract the params from the response redirect URL
        dd_client_id = query['client_id'][0]
        dd_redirect_uri = query['redirect_uri'][0]
        dd_resource = query['resource'][0]

        self.end_point = (f"{adfs_authorize_url}?" +
                          "response_type=code&" +
                          "scope=openid&" +
                          f"client_id={dd_client_id}&" +
                          f"redirect_uri={dd_redirect_uri}&" +
                          f"resource={dd_resource}")

        self.payload = (
                f"username={username}&" +
                f"password={password}&" +
                "AuthMethod=FormsAuthentication")
        self.dd_url = dd_url
        self.verify_ssl = verify_ssl
        self.proxies = proxies

    def get_bearer_token(self):
        response = requests.request("POST", self.end_point, data=self.payload, verify=self.verify_ssl,
                                    proxies=self.proxies)

        tokens = response.json()
        return tokens["data"]["token"]
