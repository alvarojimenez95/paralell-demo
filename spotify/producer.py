import asyncio 
from typing import List
from spotify_client import Spotify
from dotenv import load_dotenv
import os
import logging
from time import perf_counter
import asyncio
from pprint import pprint


logging.basicConfig(filename='app.log', filemode='w', level = logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

async def produce_work(batch_load: List[dict], queue: asyncio.Queue, check: asyncio.Event):
    c = Spotify(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    await get_track_ids(c, batch_load, queue)
    check.set()

async def get_track_ids(c: Spotify, batch_load: List[dict], queue: asyncio.Queue):
    for data in batch_load:
        track_ids = await c.get_artist_track_ids(artist_name=data["artist"])
        for track in track_ids["tracks"]["items"]:
            await queue.put({"task_id": data["task_id"], "artist" : data["artist"], "track_id": track["id"]})