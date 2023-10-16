'''
Created on May 30, 2022

@author: jevan
'''
import requests, json, urllib.parse

class GenericResourceOwnerPasswordFlow:
    
    def __init__(self, username, password, verify_ssl=True, proxies=None, auth=None) -> None:
        self.token_url = auth['idp_token_url'] if 'idp_token_url' in auth else None
        self.client_id = auth['idp_client_id'] if 'idp_client_id' in auth else None
        self.client_secret = auth['idp_client_secret'] if 'idp_client_secret' in auth else None
        self.token_key = auth['idp_token_key'] if 'idp_token_key' in auth else 'id_token'
        self.scope = auth['idp_scope'] if 'idp_scope' in auth else 'openid'
        self.payload = {'grant_type': 'password', 'scope': self.scope, 'username': username, 'password': password}
        
        self.verify_ssl = verify_ssl
        self.proxies = proxies

    def get_bearer_token(self):
        token_response = requests.post(self.token_url, 
                               data=self.payload, 
                               verify=self.verify_ssl, 
                               allow_redirects=False, 
                               auth=(urllib.parse.quote(self.client_id), self.client_secret))

        tokens = json.loads(token_response.text)

        return tokens[self.token_key]
