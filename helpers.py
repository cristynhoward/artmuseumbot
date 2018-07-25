""" Miscellaneous helper functions.
"""
from secrets import *
from os import path
from time import strftime, gmtime
import tweepy


def get_twitter_api():
    """ Use secrets to authenticate twitter API access. """
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    return tweepy.API(auth)


def get_path_to(filename):
    """ Get the path to a file by filename in the present directory.

    :param filename: The name of the file in the present directory.
    :type filename: str
    :return: The full path to the file.
    :rtype: str
    """
    dir = path.realpath(path.dirname(__file__))
    return path.join(dir, filename)


def log(message):
    """ Log a message in the bot log file.

    :param message: The message to be recorded.
    :type message: str
    :return: None
    :rtype: None
    """
    print(message)
    day = strftime("%d_%b_%Y", gmtime())
    with open(get_path_to("logs/" + day + ".log"), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)


def obj_desc(obj):
    """ Generate a description of an object in the Harvard Art Museum archives.

    :param object: JSON encoded object info as produced by the HAM API.
    :type object: dict
    :return: Description of the object.
    :rtype: str
    """
    text = obj['title'] + '\n'

    if obj['commentary'] is not None:
        text = '\n' + obj['commentary'] + '\n\n'

    if obj['peoplecount'] > 0:  # Include all artist names.
        text = text + obj['people'][0]['name']
        for i in range(1, obj['peoplecount']):
            text = text + ', ' + obj['people'][i]['name']
        text = text + '\n'

    if obj['classification'] is not None and obj['technique'] is not None:
        text = text + obj['classification'] + ', ' + obj['technique'] + '\n'
    else:
        if obj['classification'] is not None:
            text = text + obj['classification'] + '\n'
        if obj['technique'] is not None:
            text = text + obj['technique'] + '\n'

    if obj['culture'] is not None:
        text = text + obj['culture'] + ', '

    return text + obj['dated']


def exh_desc(exh):
    """

    :param exh:
    :type exh:
    :return:
    :rtype:
    """
    text = exh['title'] + '\n'
    if exh['venues'] is not None:
        for i in range(0, len(exh['venues'])):
            venue = exh['venues'][i]
            text = text + venue['name'] + ', '
            if venue['city'] is not None:
                text = text + venue['city'] + ', '
            if venue['country'] is not None:
                text = text + venue['country'] + ', '
            text = text + venue['begindate'] + ' - ' + venue['enddate'] + '\n'
    if exh['shortdescription'] is not None:
        text = text + exh['shortdescription'] + '\n'
    else:
        if exh['description'] is not None:
            text = text + exh['description'] + '\n'
    return text


def artist_desc(artist):
    """

    :param artist:
    :type artist:
    :return:
    :rtype:
    """
    text = artist['displayname'] + '\n'

    if artist['datebegin'] is not None and artist['dateend'] is not None:
        text = text + artist['datebegin']
        if artist['birthplace'] is not None:
            text = text + ", " + artist['birthplace']
        text = text + " - " + artist['dateend']
        if artist['deathplace'] is not None:
            text = text + ", " + artist['deathplace']
        text = text + '\n'

    return text + artist['culture']
