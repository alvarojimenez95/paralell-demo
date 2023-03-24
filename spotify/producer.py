import asyncio 
from typing import List

async def produce_work(batch_load: List[dict], queue: asyncio.Queue, check: asyncio.Event):
    for data in batch_load:
        await queue.put(data)
    check.set()