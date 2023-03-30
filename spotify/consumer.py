from spotify_client import Spotify
from dotenv import load_dotenv
import os
import logging
from time import perf_counter
import asyncio


logging.basicConfig(filename='app.log', filemode='w', level = logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

async def get_tracks(c:Spotify, artist: str):
    """Given an artist's name, it returns a list of track ids of songs
    for that artist"""
    track_ids = []
    tracks = await c.get_artist_track_ids(artist_name=artist)
    for track in tracks["tracks"]["items"]:
            track_ids.append(track["id"])
    logging.info(f"Total number of tracks: {len(track_ids)}")
    return track_ids


async def get_track_by_id(c: Spotify, track_id: str):
    """Given a track id, returns the track info"""
    track = await c.get_track(track_id=track_id)
    return track 

async def do_work(work_queue: asyncio.Queue, result_queue: asyncio.Queue):
    """Consumes data from the work queue and puts back the results into the result_queue. Consumer"""
    c = Spotify(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    while True:
        task_data = await work_queue.get()
        task_id = task_data["task_id"]
        artist = task_data["artist"]
        # get the tracks
        track_ids = await get_tracks(c, artist)
        for track_id in track_ids:
             start = perf_counter()
             logging.info(f"{artist} - {track_id}")
             # get the audio features
             track_data = await c.get_audio_features(track_id)
             end = perf_counter()
             # put back the result into the result queue
             await result_queue.put(
                  {
                  "task_id" : task_id,
                  "id" : track_data["id"],
                  "artist" : artist,
                  "loudness" : track_data["loudness"],
                  "acousticness" : track_data["acousticness"],
                  "instrumentalness" : track_data["instrumentalness"],
                  "tempo" : track_data["tempo"],
                  "liveness" : track_data["liveness"],
                  "energy" : track_data["energy"],
                  "danceability" : track_data["danceability"],
                  "time_secs" : end-start
                  }
             )
        # finish task
        work_queue.task_done()