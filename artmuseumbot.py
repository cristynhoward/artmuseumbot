""" First attempt to play around with art museum API.
"""
from descriptions import obj_desc
from secrets import *
from helpers import *
import requests
import random
import tweepy


def tweet_random_object():
    """  Access the HAM API, try to find a suitable object to tweet, and tweet it.

    :return: The result of attempting to tweet, or False if unsuccessful.
    :rtype: tweepy.Status, tweepy.TweepError, None
    """
    log("Accessing HAM API.")
    url = 'https://api.harvardartmuseums.org/object?apikey=' + API_KEY \
          + '&hasimage=1&size=1&sort=random&q=totalpageviews:' + str(random.randint(0, 1000))
    object_page = requests.get(url)
    if object_page.status_code == 200:
        json = object_page.json()

        if json['info']['totalrecords'] > 0:  # If at least one object record returned...
            obj = json['records'][0]
            if len(obj['images']) > 0:  # If object record contains image...

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
                    try:
                        bot_tweet = api.update_with_media(imagefile, text)
                    except tweepy.error.TweepError as e:
                        log('Encountered TweepError:' + e.response.text)
                        return False
                    else:
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


def attempt_to_tweet_object(total_attempts):
    """ Attempt to tweet an archive object.

    :param total_attempts: The total number of times to try to tweet.
    :type total_attempts: int
    :return: None
    """
    tweeted = False
    attempts = total_attempts

    while tweeted is False and attempts > 0:
        log('Tweet attempt #' + str(total_attempts - attempts + 1))
        tweeted = tweet_random_object()
        attempts -= 1


if __name__ == '__main__':
    attempt_to_tweet_object(10)

