import asyncio 
from time import perf_counter
from typing import Callable, List 
import consumer 
import producer 
import result_handler

NUM_WORKERS = 5
WORK_QUEUE_MAX_SIZE = 50
NUM_RESULT_HANDLERS = 50
RESULT_QUEUE_MAX_SIZE = 50

async def _controller(batch_load: List[dict], task_completed_callback: Callable, job_completed_callback: Callable) -> None:
    """Given a batch load, sets the workload"""
    start = perf_counter()
    work_queue = asyncio.Queue(maxsize=WORK_QUEUE_MAX_SIZE) # create work queue 
    result_queue = asyncio.Queue(maxsize=RESULT_QUEUE_MAX_SIZE) # create result queue

    tasks = [] # initialise tasks 

    producer_completed = asyncio.Event() # set producer event to false
    producer_completed.clear()
    # start producer
    tasks.append(
        asyncio.create_task(producer.produce_work(batch_load, work_queue, producer_completed))
    )
    # start consumers
    for _ in range(NUM_WORKERS):
        tasks.append(
            asyncio.create_task(consumer.do_work(work_queue, result_queue))
        )
    # start result handlers
    for _ in range(NUM_RESULT_HANDLERS):
        tasks.append(
            asyncio.create_task(result_handler.handle_task_result(result_queue, task_completed_callback))
        )
    await producer_completed.wait()
    await work_queue.join()
    await result_queue.join()

    # cancel the tasks
    for task in tasks:
        task.cancel()
    
    end = perf_counter()
    job_completed_callback({"elapsed_secs" : end - start})

def run_job(batch_load: List[dict], task_completed_callback: Callable, job_completed_callback: Callable) -> None:
    """Runs the controller"""
    asyncio.run(_controller(batch_load, task_completed_callback, job_completed_callback))