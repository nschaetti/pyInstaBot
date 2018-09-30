#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Imports
import pyInstaBot
from textblob import TextBlob
import time
import logging
import pyInstaBot.tools.strings as pystr
import pyInstaBot.instagram
import random


# Class to find media to like or comment
class MediaFinder(object):
    """
    Class to find media to like or comment
    """

    # Constructor
    def __init__(self, search_keywords="", depth=20, shuffle=False, polarity=0.0, subjectivity=0.5, languages=['en']):
        """
        Constructor
        """
        # Properties
        self._search_keywords = search_keywords
        self._polarity = polarity
        self._subjectivity = subjectivity
        self._languages = languages
        self._depth = depth
        self._level = 0

        # Feed
        self._medias = list()

        # Pagination
        self._max_id = ''

        # Shuffle
        if shuffle:
            random.shuffle(self._medias)
        # end if
    # end __init__

    #############################################
    # Override
    #############################################

    # Iterator
    def __iter__(self):
        """
        Iterator
        :return:
        """
        return self
    # end __iter__

    # Next
    def next(self):
        """
        Next element
        :return:
        """
        if len(self._medias) <= 0:
            # Stop if end
            if self._max_id is None:
                raise StopIteration()
            # end if

            # Get medias
            hashtag_feed = pyInstaBot.instagram.InstagramConnector().hashtag_feed(self._search_keywords, maxid=self._max_id)

            # Type
            if type(hashtag_feed) is bool:
                raise StopIteration()
            # end if

            # Items
            self._medias = hashtag_feed['items']
            self._level += 1

            # Stop
            if self._level >= self._depth:
                raise StopIteration()
            # end if

            # Next max id
            if 'next_max_id' in hashtag_feed:
                self._max_id = hashtag_feed['next_max_id']
            else:
                self._max_id = None
            # end if
        # end if

        # Current media
        current_media = self._medias[0]

        # Remove
        self._medias.remove(current_media)

        # Return
        return current_media
    # end next

    # To unicode
    def __unicode__(self):
        """
        To unicode
        :return:
        """
        return u"MediaFinder({})".format(self._search_keywords)
    # end __unicode__

    # To str
    def __str__(self):
        """
        To str
        :return:
        """
        return "MediaFinder({})".format(self._search_keywords)
    # end __str__

    ############################################
    # Private
    ############################################

# end TweetFinder
