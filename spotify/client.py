import requests
from typing import Optional, List, Mapping
from base64 import b64encode, b64decode
from pprint import pprint
from urllib.parse import urlparse, parse_qs
import webbrowser

class HTTPClient:
    token_url = "https://accounts.spotify.com/api/token"
    base_url = "https://api.spotify.com/v1"
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self._session = requests.Session()

    def _pepare_header(self):
        encoded_credentials = b64encode(f"{self.client_id}:{self.client_secret}".encode('utf-8')).decode("ascii")
        return {"Authorization" : f"Basic {encoded_credentials}", "Content-Type" : "application/x-www-form-urlencoded"}
    
    def retrieve_token(self):
        headers = self._pepare_header()
        resp = requests.post(self.token_url, headers = headers, params = {"grant_type" : "client_credentials"})
        resp.raise_for_status()
        self.token = resp.json()["access_token"]

    def call(self, method, endpoint, params = None, body = None, headers = None):
        url = self.base_url + endpoint
        if headers:
            headers.update(self._prepare_auth_header())
        else:
            headers = self._prepare_auth_header()
        with self._session as session:
            resp = session.request(method = method, url = url, params = params, headers = headers, json = body)
            resp.raise_for_status()
            return resp.json()
        
    def get(self, endpoint, params = None, headers = None):
        return self.call("GET", endpoint, params, headers = headers)
    
    def _prepare_auth_header(self):
        return {"Authorization" : f"Bearer {self.token}"}

        


    
