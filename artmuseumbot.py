""" First attempt to play around with art museum API.
"""
from secrets import *
from helpers import *
import requests
import random


def tweet_random_object():
    """

    :return:
    :rtype:
    """
    print("Accessing HAM API.")
    url = 'https://api.harvardartmuseums.org/object?apikey=' + API_KEY \
          + '&hasimage=1&size=1&sort=random&q=totalpageviews:' + str(random.randint(0,1000))
    object_page = requests.get(url)

    if object_page.status_code == 200:
        json = object_page.json()

        if json['info']['totalrecords'] > 0:
            obj = json['records'][0]
            if obj['imagecount'] > 0:
                imageurl = obj['images'][0]['baseimageurl']
                image_page = requests.get(imageurl)
                imagefile = 'temporary.jpg'

                if image_page.status_code == 200:
                    print("Found object with image.")
                    print(imageurl)
                    with open(imagefile, 'wb') as image:
                        for imgdata in image_page:
                            image.write(imgdata)

                    api = get_twitter_api()
                    api.update_with_media(imagefile, obj_desc(obj))
                    return True


def exhibition_exploration():
    exh_url = 'https://api.harvardartmuseums.org/exhibition?apikey=' + API_KEY + '&hasimage=1&size=1&sort=random'
    exh_json = requests.get(exh_url).json()
    exh = exh_json['records'][0]
    print(exh_desc(exh))

    obj_url = 'https://api.harvardartmuseums.org/object?apikey=' + API_KEY \
                  + '&hasimage=1&sort=random&exhibition=' + str(exh['id'])
    obj_json = requests.get(obj_url).json()
    for i in range(0, len(obj_json['records'])):
        obj_info = obj_json['records'][i]
        print(obj_desc(obj_info))


def artist_exploration():
    artist_url = 'https://api.harvardartmuseums.org/person?apikey=' + API_KEY + '&size=1&sort=random'
    artist_json = requests.get(artist_url).json()
    artist = artist_json['records'][0]
    if artist['objectcount'] is not None and artist['objectcount'] > 4:
        print(artist_desc(artist))


if __name__ == '__main__':
    tweeted = False
    while tweeted is False:
        tweeted = tweet_random_object()
