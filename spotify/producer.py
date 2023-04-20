import asyncio 
from typing import List
from localhost import SpotifyLocalHost
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

async def produce_work(batch_load, queue: asyncio.Queue, check: asyncio.Event):
    # check is a parameter event that is used to signal the end of the work
    await get_track_ids(batch_load, queue) # await for the queue to be filled
    check.set() # signal the end of the work

async def get_track_ids(batch_load, queue: asyncio.Queue):
    """Puts items on the queue. Producer"""
    for i, track in enumerate(batch_load):
            await queue.put({"task_id" : i, "track_id": track["track_id"]})