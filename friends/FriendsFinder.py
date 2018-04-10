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


# Class to find new users to follow
class FriendsFinder(object):
    """
    Class to find new users to follow
    """

    # Constructor
    def __init__(self, hashtag="", shuffle=True, polarity=0.0, subjectivity=0.5, languages=['en']):
        """
        Constructor
        """
        # Properties
        self._hashtag = hashtag
        self._polarity = polarity
        self._subjectivity = subjectivity
        self._languages = languages

        # Feed
        feed = pyInstaBot.instagram.InstagramConnector().hashtag_feed(hashtag)

        # Load users
        self._users = list()
        self._user_names = list()
        for media in feed['ranked_items']:
            user = media['user']
            if not user['has_anonymous_profile_picture'] and not user['friendship_status']['following'] and not user['friendship_status']['outgoing_request']:
                if user['username'] not in self._user_names:
                    info = pyInstaBot.instagram.InstagramConnector().username_info(user['pk'])
                    user['biography'] = info['user']['biography']
                    self._users.append(user)
                    self._user_names.append(user['username'])
                # end if
            # end if
        # end for

        # Shuffle
        if shuffle:
            random.shuffle(self._users)
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
        if len(self._users) <= 0:
            raise StopIteration()
        # end if

        # Current media
        current_media = self._users[0]

        # Remove
        self._users.remove(current_media)

        # Return
        return current_media
    # end next

    # To unicode
    def __unicode__(self):
        """
        To unicode
        :return:
        """
        return u"FriendsFinder({})".format(self._hashtag)
    # end __unicode__

    # To str
    def __str__(self):
        """
        To str
        :return:
        """
        return "FriendsFinder({})".format(self._hashtag)
    # end __str__

    ############################################
    # Private
    ############################################

# end FriendsFinder
