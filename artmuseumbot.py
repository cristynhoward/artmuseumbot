""" First attempt to play around with art museum API.
"""
from secrets import *
from helpers import *
import tweepy
import requests
import random


def tweet_random_object():
    """  Access the HAM API, try to find a suitable object to tweet, and tweet it.

    :return: The result of attempting to tweet, or False if unsuccessful.
    :rtype: tweepy.Status, tweepy.TweepError, None
    """
    log("Accessing HAM API.")
    url = 'https://api.harvardartmuseums.org/object?apikey=' + API_KEY \
          + '&hasimage=1&size=1&sort=random&q=totalpageviews:' + str(random.randint(0,1000))
    object_page = requests.get(url)
    if object_page.status_code == 200:
        json = object_page.json()

        if json['info']['totalrecords'] > 0:  # If at least one object record returned...
            obj = json['records'][0]
            if obj['imagecount'] > 0:  # If object record contains image...

                # Attempt to connect to image url...
                imageurl = obj['images'][0]['baseimageurl']
                image_page = requests.get(imageurl)
                if image_page.status_code == 200:

                    # Download image.
                    imagefile = 'temporary.jpg'
                    with open(imagefile, 'wb') as image:
                        for imgdata in image_page:
                            image.write(imgdata)
                    log("Found object with image: " + imageurl)

                    # Tweet.
                    text = obj_desc(obj)
                    api = get_twitter_api()
                    bot_tweet = api.update_with_media(imagefile, text)
                    print(str(bot_tweet is not tweepy.TweepError))
                    if bot_tweet is not tweepy.TweepError:
                        log('Tweeted: ' + text)
                        return bot_tweet

                else:
                    log('Could not access image page.')
                    return False
            else:
                log('Object record contains no images.')
                return False
        else:
            log('API returned no object records.')
            return False
    else:
        log('Could not access HAM API.')
        return False


def exhibition_exploration():
    # Experimental exploration of exhibition API features.
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
    # Experimental exploration of artist API features.
    artist_url = 'https://api.harvardartmuseums.org/person?apikey=' + API_KEY + '&size=1&sort=random'
    artist_json = requests.get(artist_url).json()
    artist = artist_json['records'][0]
    if artist['objectcount'] is not None and artist['objectcount'] > 4:
        print(artist_desc(artist))


if __name__ == '__main__':
    tweeted = False
    while tweeted is False:
        tweeted = tweet_random_object()
