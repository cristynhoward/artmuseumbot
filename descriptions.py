""" Module containing methods to generate descriptions of objects, venues, artists, exhibitions, etc.
"""


def obj_desc(obj):
    """ Generate a description of an object in the Harvard Art Museum archives.

    :param obj: JSON encoded object info as produced by the HAM API.
    See: https://github.com/harvardartmuseums/api-docs/blob/master/object.md
    :type obj: dict
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
    """ Generate a description of an exhibition.

    :param exh: Exhibition record from HAM API.
    See: https://github.com/harvardartmuseums/api-docs/blob/master/exhibition.md
    :type exh: dict
    :return: Description of exhibition.
    :rtype: str
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
    """ Generate a description of an artist.

    :param artist: Artist record from HAM API.
    See: https://github.com/harvardartmuseums/api-docs/blob/master/person.md
    :type artist: dict
    :return: Description of artist.
    :rtype: str
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
