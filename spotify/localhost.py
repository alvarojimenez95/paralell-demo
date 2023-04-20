import aiohttp 
import logging
import asyncio 

class SpotifyLocalHost:
    url = "http://127.0.0.1:8000"
    def __init__(self):
        pass
    async def get_tracks(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url + "/tracks/") as resp:
                json_string = await resp.json()
                return json_string
    
    async def get_track_audio_features(self, track_id: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url + "/audio-features/" + track_id) as resp:
                json_string = await resp.json()
                return json_string
    
