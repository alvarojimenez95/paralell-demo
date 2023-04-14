from dotenv import load_dotenv
import os
from pprint import pprint 
import logging
from functools import partial
from controller import run_job
from uuid import uuid4
import pandas as pd


logging.basicConfig(filename='app.log', filemode='w', level = logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

ARTISTS = [
    "Talking Heads",
    "Carl Perkins",
    "Curtis Mayfield",
    "R.E.M.",
    "Diana Ross and the Supremes",
    "Lynyrd Skynyrd",
    "Nine Inch Nails",
    "Booker T. and the MGs",
    "Guns n’ Roses",
    "Tom Petty",
    "Carlos Santana",
    "The Yardbirds",
    "Jay-Z",
    "Gram Parsons",
    "Tupac Shakur",
    "Black Sabbath",
    "James Taylor",
    "Eminem",
    "Creedence Clearwater Revival",
    "The Drifters",
    "Elvis Costello",
    "The Four Tops",
    "The Stooges",
    "Beastie Boys",
    "The Shirelles",
    "Eagles",
    "Hank Williams",
    "Hank Williams",
    "AC/DC",
    "Frank Zappa",
    "The Police",
    "Jackie Wilson",
    "The Temptations",
    "Cream",
    "Al Green",
    "The Kinks",
    "Phil Spector",
    "Tina Turner",
    "Joni Mitchell",
    "Metallica",
    "The Sex Pistols",
    "Aerosmith",
    "Parliament and Funkadelic",
    "Grateful Dead",
    "Dr. Dre",
    "Eric Clapton",
    "Howlin’ Wolf",
    "The Allman Brothers Band",
    "Queen",
    "Pink Floyd",
    "Simon and Garfunkel",
    "David Bowie",
    "John Lennon",
    "Roy Orbison",
    "Madonna",
    "Michael Jackson",
    "Neil Young",
    "The Everly Brothers",
    "Smokey Robinson and the Miracles",
    "Johnny Cash",
    "Nirvana",
    "The Who",
    "The Clash",
    "Prince",
    "The Ramones",
    "Fats Domino",
    "Jerry Lee Lewis",
    "Bruce Springsteen",
    "U2",
    "Otis Redding",
    "Bo Diddley",
    "The Velvet Underground",
    "Marvin Gaye",
    "Muddy Waters",
    "Sam Cooke",
    "Stevie Wonder",
    "Led Zeppelin",
    "Buddy Holly",
    "The Beach Boys",
    "Bob Marley",
    "Ray Charles",
    "Aretha Franklin",
    "Little Richard",
    "James Brown",
    "Jimi Hendrix",
    "Chuck Berry",
    "The Rolling Stones",
    "Elvis Presley",
    "Bob Dylan",
    "The Beatles"
]

COLUMNS =[
        "task_id",
            "id",
            "artist" ,
            "loudness",
            "acousticness",
            "instrumentalness" ,
            "tempo" ,
            "liveness", 
            "energy" ,
            "danceability",
            "time_secs"]
def main(job_id: str) -> None:
    print(f"Starting job {job_id}")
    task_callback = partial(task_completed_callback_handler, job_id)
    job_callback = partial(job_completed_callback_handler, job_id)
    # set the task data
    task_data = [
        {"task_id" : i, "artist" : artist} for i, artist in enumerate(ARTISTS[:10])
    ]

    data = run_job(task_data, task_callback, job_callback)
    pprint(data)


def task_completed_callback_handler(job_id: str, callback_message: dict)-> None:
    pprint(f"Task completed in {job_id=}: {callback_message=}")
    return callback_message

def job_completed_callback_handler(job_id: str, callback_message: dict)-> None:
    pprint(f"Job completed in {job_id=}: {callback_message=}")
    return callback_message


if __name__ == "__main__":
    df = pd.DataFrame(columns = COLUMNS)
    main(job_id = str(uuid4()))
