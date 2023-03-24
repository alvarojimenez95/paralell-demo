from spotify_client import Spotify
from dotenv import load_dotenv
import os
from pprint import pprint 
import logging
from time import perf_counter
import asyncio


logging.basicConfig(filename='app.log', filemode='w', level = logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

async def get_tracks(c:Spotify, artist: str):
    track_ids = []
    tracks = await c.get_artist_track_ids(artist_name=artist)
    for track in tracks["tracks"]["items"]:
            track_ids.append(track["id"])
    logging.info(f"Total number of tracks: {len(track_ids)}")
    return track_ids


async def get_track_by_id(c: Spotify, track_id: str):
    track = await c.get_track(track_id=track_id)
    return track 

async def do_work(work_queue: asyncio.Queue, result_queue: asyncio.Queue):
    c = Spotify(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    while True:
        task_data = await work_queue.get()
        task_id = task_data["task_id"]
        artist = task_data["artist"]
        start = perf_counter()
        track_ids = await get_tracks(c, artist)
        end = perf_counter()
        await result_queue.put(
             {
                "task_id" : task_id,
                "track_ids" : track_ids,
                "time_secs" : end- start,
                "artist" : artist
             }
        )
        work_queue.task_done()