""" Experimental exploration of API features.
"""
from descriptions import *
from helpers import *
import requests


def exhibition_exploration():
    # Experimental exploration of exhibition API features.
    exh_url = 'https://api.harvardartmuseums.org/exhibition?apikey=' + API_KEY + '&hasimage=1&size=1&sort=random'
    exh_json = requests.get(exh_url).json()
    exh = exh_json['records'][0]
    print(exh_desc(exh))
    # Get objects from the exhibition.
    obj_url = 'https://api.harvardartmuseums.org/object?apikey=' + API_KEY \
                  + '&hasimage=1&sort=random&exhibition=' + str(exh['id'])
    obj_json = requests.get(obj_url).json()
    for i in range(0, len(obj_json['records'])):
        obj_info = obj_json['records'][i]
        print(obj_desc(obj_info))


def artist_exploration():
    # Experimental exploration of artist API features.
    artist_url = 'https://api.harvardartmuseums.org/person?apikey=' + API_KEY + '&size=1&sort=random'
    artist_json = requests.get(artist_url).json()
    artist = artist_json['records'][0]
    if artist['objectcount'] is not None and artist['objectcount'] > 4:
        print(artist_desc(artist))
