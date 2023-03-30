from client import HTTPClient
import requests
from pprint import pprint
class Spotify:
    def __init__(self, client_id: str, client_secret: str):
        self.client = HTTPClient(client_id=client_id, client_secret=client_secret)
        self.client.retrieve_token()

    def _prepare_header(self):
        return {"Authorization" : f"Bearer {self.client.token}"}

    def get_track(self, track_id: str):
        headers = self._prepare_header()
        url = f"https://api.spotify.com/v1/tracks/{track_id}"
        resp = requests.get(url = url, headers=headers)
        return resp.json() 
    
    def get_artist(self, artist_id: str):
        headers = self._prepare_header()
        url = f"https://api.spotify.com/v1/artists/{artist_id}"
        resp = requests.get(url = url, headers = headers)
        return resp.json()


    def get_artist_track_ids(self, artist_name: str = None, number: int = 100):
        headers = self._prepare_header()
        url = f"https://api.spotify.com/v1/search"
        offset = 0
        # track_ids = []
        # while offset < number:
        params = {"limit" : 20, "q" : artist_name, "type": "track"}
        resp = requests.get(url = url, params = params, headers = headers)
        return resp.json()
    

    def get_audio_features(self, track_id: str):
        endpoint = f"https://api.spotify.com/v1/audio-features/{track_id}"
        resp = requests.get(url = endpoint)
        return resp.json()
