class KeyCloakResourceOwnerPassword:
    def __init__(self, ze_http_client, dd_url, token_url, username, password, idp_client_id, idp_client_secret,
                 verify_ssl=True, proxies=None) -> None:
        self.ze_http_client = ze_http_client
        self.verify_ssl = verify_ssl
        self.username = username
        self.password = password
        self.proxies = proxies
        self.token_url = token_url
        # http://localhost:8080/auth/realms/zema/protocol/openid-connect/token
        self.idp_client_id = idp_client_id

    def authenticate(self):
        headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }

        payload = {'username': self.username,
                   'password': self.password,
                   'client_id': self.idp_client_id,
                   'grant_type': 'password'
                   }

        response = self.ze_http_client.post(self.token_url, data=payload, proxies=self.ze_http_client.proxies,
                                            headers=headers, verify=self.verify_ssl)

        tokens = response.json()
        return tokens["access_token"]
