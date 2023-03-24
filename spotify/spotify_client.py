from client import HTTPClient
import requests
from pprint import pprint
import logging
class Spotify:
    def __init__(self, client_id: str, client_secret: str):
        self.client = HTTPClient(client_id=client_id, client_secret=client_secret)
        self.client.retrieve_token()

    async def get_track(self, track_id: str):
        endpoint = f"/tracks/{track_id}"
        resp = await self.client.get(endpoint = endpoint)
        logging.info(f"Song: {resp['name']}. Artist: {resp['artists'][0]['name']}")
        return {"name" : resp["name"], "artist" : resp["artists"][0]["name"]}
    
    async def get_artist(self, artist_id: str):
        endpoint = f"/artists/{artist_id}"
        resp = await self.client.get(endpoint = endpoint)
        return resp


    async def get_artist_track_ids(self, artist_name: str = None, number: int = 100):
        endpoint = "/search"
        params = {"limit" : 20, "q" : artist_name, "type": "track"}
        resp = await self.client.get(endpoint = endpoint, params = params)
        return resp