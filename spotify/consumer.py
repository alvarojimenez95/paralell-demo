from pprint import pprint
from localhost import SpotifyLocalHost
from dotenv import load_dotenv
import os
import logging
from time import perf_counter
import asyncio


logging.basicConfig(filename='app.log', filemode='w', level = logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

async def get_tracks(c:SpotifyLocalHost, artist: str):
    """Given an artist's name, it returns a list of track ids of songs
    for that artist"""
    track_ids = []
    tracks = await c.get_artist_track_ids(artist_name=artist)
    for track in tracks:
            track_ids.append(track["track_id"])
    logging.info(f"Total number of tracks: {len(track_ids)}")
    return track_ids

async def do_work(work_queue: asyncio.Queue, result_queue: asyncio.Queue):
    """Consumes data from the work queue and puts back the results into the result_queue. Consumer"""
    c = SpotifyLocalHost()
    counter = 1
    while True:
        task_data = await work_queue.get()
        track_id = task_data["track_id"]
        # get the tracks
        start = perf_counter()
        track_audio_features = await c.get_track_audio_features(track_id)
        end = perf_counter()
        # put back the result into the result queue
        logging.info(f"Track: {track_id}. Link: {track_audio_features['track_href']}")
        queue_item = {
            "track_id" : track_id,
            "index" : counter,
            "loudness" : track_audio_features["loudness"],
            "acousticness" : track_audio_features["acousticness"],
            "instrumentalness" : track_audio_features["instrumentalness"],
            "tempo" : track_audio_features["tempo"],
            "liveness" : track_audio_features["liveness"],
            "energy" : track_audio_features["energy"],
            "danceability" : track_audio_features["danceability"],
            "time_secs" : end-start
            }
        await result_queue.put(
            queue_item
        )
        counter+=1
        # finish task
        work_queue.task_done()