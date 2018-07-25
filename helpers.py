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
