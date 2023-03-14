import requests
from requests.adapters import HTTPAdapter, Retry
from typing import Optional, List, Mapping
from base64 import b64encode, b64decode
from pprint import pprint
from urllib.parse import urlparse, parse_qs
import webbrowser
import aiohttp
import asyncio

class HTTPClient:
    token_url = "https://accounts.spotify.com/api/token"
    base_url = "https://api.spotify.com/v1"
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.retry_times  = 7
        self.backoff_factor = 0.8

    def _pepare_header(self):
        encoded_credentials = b64encode(f"{self.client_id}:{self.client_secret}".encode('utf-8')).decode("ascii")
        return {"Authorization" : f"Basic {encoded_credentials}", "Content-Type" : "application/x-www-form-urlencoded"}
    
    def retrieve_token(self):
        headers = self._pepare_header()
        resp = requests.post(self.token_url, headers = headers, params = {"grant_type" : "client_credentials"})
        resp.raise_for_status()
        self.token = resp.json()["access_token"]

    async def call(self, method, endpoint, params = None, body = None, headers = None):
        url = self.base_url + endpoint
        if headers:
            headers.update(self._prepare_auth_header())
        else:
            headers = self._prepare_auth_header()
        retry_count = 0
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.request(
                        method = method,
                        url = url,
                        json = body,
                        params = params,
                        headers = headers
                    ) as resp:
                        if resp.status in [
                            503,
                            500,
                            429,
                            406
                        ]:
                            if retry_count < self.retry_times:
                                retry_count += 1
                                await asyncio.sleep(retry_count * self.backoff_factor)
                                continue
                            else:
                                resp.raise_for_status()
                        resp.raise_for_status()
                        json = await resp.json()
                        return json
            except Exception as err:
                raise err  
        
    async def get(self, endpoint, params = None, headers = None):
        data = await self.call("GET", endpoint, params, headers = headers)
        return data
    
    def _prepare_auth_header(self):
        return {"Authorization" : f"Bearer {self.token}"}

        


    
