from client import HTTPClient
from spotify_client import Spotify
from dotenv import load_dotenv
import os
from pprint import pprint 
import logging
import asyncio

logging.basicConfig(filename='app.log', filemode='w', level = logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
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

async def get_tracks():
    c = Spotify(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    track_ids = []
    for idx, artist in enumerate(ARTISTS[:5]):
        logging.info(artist)
        tracks = await c.get_artist_track_ids(artist_name=artist)
        for track in tracks["tracks"]["items"]:
            track_ids.append(track["id"])
    logging.info(f"Total number of artists: {len(track_ids)}")
    return track_ids

async def get_track_by_id(c: Spotify, track_id: str):
    track = await c.get_track(track_id=track_id)
    return track 

async def gather_tasks(track_ids):
    c = Spotify(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    tasks = [asyncio.create_task(get_track_by_id(c, track_id)) for track_id in track_ids]
    results = await asyncio.gather(*tasks)
    return results

def main():
    import cProfile
    import pstats
    with cProfile.Profile() as pr:

        tracks = asyncio.run(get_tracks())
        asyncio.run(gather_tasks(tracks))
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename="profiling.prof")

if __name__ == "__main__":

    from time import perf_counter
    start = perf_counter()
    main()
    end = perf_counter()
    logging.info(f"Time elapsed: {end - start} seconds")
