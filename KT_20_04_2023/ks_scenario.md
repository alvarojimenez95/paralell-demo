# Scenario

We work for Spotify, and one of our clients wants better recommendations for music ads in our platform.

We are given a target audience, and want to extract information about the users track recommendations.

We routinely want to check our database and order the most listened artists for the users in the target audience, track
metrics of those tracks, and generate recommendations for background music for our client ads.

We would also like to filter the data obtained by attributes that are not desirable for an ad, like high volume or speechiness.

# Simulation 1

To simulate the scenario, we present a list of artists. For each artist, we will get 20 tracks from the artist, and for each track,
get the audio features of the track using Spotify's API.

# Simulation 2

Using a text file containing a list of track_ids, we simulate Spotify's `audio-features` endpoint to provide an example of a Producer/Consumer model that has no issues with API rate limits.
