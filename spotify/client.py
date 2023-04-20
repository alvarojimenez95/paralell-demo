import requests
from base64 import b64encode
class HTTPClient:
    token_url = "https://accounts.spotify.com/api/token"
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None

    def _pepare_header(self):
        encoded_credentials = b64encode(f"{self.client_id}:{self.client_secret}".encode('utf-8')).decode("ascii")
        return {"Authorization" : f"Basic {encoded_credentials}", "Content-Type" : "application/x-www-form-urlencoded"}
    
    def retrieve_token(self):
        headers = self._pepare_header()
        resp = requests.post(self.token_url, headers = headers, params = {"grant_type" : "client_credentials"})
        resp.raise_for_status()
        self.token = resp.json()["access_token"]
    

        


    
