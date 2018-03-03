#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Imports
import pyInstaBot
from textblob import TextBlob
import time
import logging
import pyInstaBot.tools.strings as pystr


# Class to find media to like or comment
class MediaFinder(object):
    """
    Class to find media to like or comment
    """

    # Constructor
    def __init__(self, search_keywords="", polarity=0.0, subjectivity=0.5, languages=['en']):
        """
        Constructor
        """
        # Properties
        self._search_keywords = search_keywords
        self._polarity = polarity
        self._subjectivity = subjectivity
        self._languages = languages

        # Cursor
        if search_keywords == "":
            # self._cursor = pyInstaBot.instagram.InstagramConnector().get_time_line(n_pages)
            pass
        else:
            # self._cursor = pyInstaBot.instagram.InstagramConnector().search_tweets(search_keywords, n_pages)
            pass
        # end if

        # Current list of medias
        self._medias = list()
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
        # Load if needed
        while len(self._medias) == 0:
            self._load_medias()
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

    # Get medias
    def _load_medias(self):
        """
        Get medias
        :return: A tweet
        """
        # Get page
        page = self._cursor.next()

        # Get all tweets
        for tweet in page:
            # if not tweet.retweeted and 'RT @' not in tweet.text:
            if not tweet.retweeted:
                # Analyze text
                tweet_blob = TextBlob(tweet.text)

                # Pass level of pol & sub
                if tweet_blob.sentiment.polarity >= self._polarity and \
                    tweet_blob.sentiment.subjectivity <= self._subjectivity and \
                    tweet_blob.detect_language() in self._languages:
                    self._medias.append((tweet, tweet_blob.sentiment.polarity, tweet_blob.sentiment.subjectivity))
                # end if
        # end for

        # Wait
        logging.getLogger(pystr.LOGGER).info(u"Waiting 60 seconds...")
        time.sleep(60)
    # end _load_tweets

# end TweetFinder
