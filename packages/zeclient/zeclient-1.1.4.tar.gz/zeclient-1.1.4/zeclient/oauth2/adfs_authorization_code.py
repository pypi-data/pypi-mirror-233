class AdfsAuthorizationCode:
    def __init__(self, ze_http_client, dd_url, username, password, verify_ssl=True) -> None:
        self.dd_authorize_url = dd_url + "/oauth2/authorize"
        self.ze_http_client = ze_http_client
        self.verify_ssl = verify_ssl
        self.username = username
        self.password = password
        pass

    def authenticate(self):
        session = self.ze_http_client.session
        response = self.ze_http_client.get(self.dd_authorize_url)

        adfs_authorize_url = response.url

        payload = {'UserName': self.username,
                   'Password': self.password,
                   'AuthMethod': 'FormsAuthentication'}

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = self.ze_http_client.post(adfs_authorize_url, data=payload, proxies=self.ze_http_client.proxies,
                                            headers=headers)
