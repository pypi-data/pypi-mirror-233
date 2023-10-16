import base64


class OktaResourceOwnerPassword:
    def __init__(self, ze_http_client, okta_issuer_url, username, password, idp_client_id, idp_client_secret,
                 verify_ssl=True) -> None:
        self.okta_token_url = okta_issuer_url + "/v1/token"
        self.ze_http_client = ze_http_client
        self.verify_ssl = verify_ssl
        self.username = username
        self.password = password
        self.idp_client_id = idp_client_id
        self.idp_client_secret = idp_client_secret
        pass

    def get_access_token(self):
        session = self.ze_http_client.session

        payload = {'username': self.username,
                   'password': self.password,
                   'grant_type': 'password',
                   'scope': 'openid'}

        code = f'{self.idp_client_id}:{self.idp_client_secret}'
        encoded = base64.b64encode(code.encode('ascii')).decode('ascii')

        headers = {
            'authorization': f'Basic {encoded}',
            'content-type': 'application/x-www-form-urlencoded'
        }
        response = self.ze_http_client.post(self.okta_token_url, data=payload, proxies=self.ze_http_client.proxies,
                                            headers=headers)

        tokens = response.json()
        return tokens["access_token"]
