import aiohttp 
import logging
import asyncio 

class SpotifyLocalHost:
    url = "http://127.0.0.1:8000"
    def __init__(self):
        self.session = None 

    def __del__(self):
        if self.session:
            asyncio.run(self.session.close())
    async def get_tracks(self):
        resp = await self.session.get(self.url + "/tracks")
        json_string = await resp.json()
        return json_string
    
