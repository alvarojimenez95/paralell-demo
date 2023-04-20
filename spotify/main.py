from dotenv import load_dotenv
import os
from pprint import pprint 
import logging
from functools import partial
from controller import run_job
from uuid import uuid4


logging.basicConfig(filename='app.log', filemode='w', level = logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


def main(job_id: str) -> None:
    import cProfile
    import pstats
    with cProfile.Profile() as pr:

        print(f"Starting job {job_id}")
        task_callback = partial(task_completed_callback_handler, job_id)
        job_callback = partial(job_completed_callback_handler, job_id)
        # set the task data
        track_ids = []
        with open("/Users/alvaro/dev/sandbox/paralell-demo/track_ids.txt", "r") as f:
            track_ids = f.readlines()
        task_data = [
            {"track_id" : track_id.replace("\n", "")} for _, track_id in enumerate(track_ids)
        ]

        run_job(task_data, task_callback, job_callback)
    stats = pstats.Stats(pr)
    stats.dump_stats(filename="profile.prof")


def task_completed_callback_handler(job_id: str, callback_message: dict)-> None:
    pprint(f"Task completed in {job_id =}: {callback_message=}")

def job_completed_callback_handler(job_id: str, callback_message: dict)-> None:
    pprint(f"Job completed in {job_id=}: {callback_message=}")


if __name__ == "__main__":
    main(job_id = str(uuid4()))
