#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : twitter.TweetBotConnector.py
# Description : Main class to connect with Twitter API.
# Auteur : Nils Schaetti <n.schaetti@gmail.com>
# Date : 01.05.2017 17:59:05
# Lieu : Nyon, Suisse
#
# This file is part of the pyTweetBot.
# The pyTweetBot is a set of free software:
# you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyTweetBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with pyTweetBar.  If not, see <http://www.gnu.org/licenses/>.
#

import datetime
import logging
from pyInstaBot.patterns.singleton import singleton
import pyInstaBot.tools.strings as pystr
from InstagramAPI import InstagramAPI
import os
import json


# Request limits reached.
class RequestLimitReached(Exception):
    """
    Exception raised when some limits are reached.
    """
    pass
# end RequestLimitReached


# Main class to connect with Twitter API
@singleton
class InstagramConnector(object):
    """
    Twitter Connector
    """

    # Constructor
    def __init__(self, session_file, bot_config=None):
        """
        Constructor
        :param bot_config: Bot configuration object.
        """
        # Auth to Instagram
        self.session_file = session_file
        config = bot_config.instagram
        self._instagram = InstagramAPI(username=config['username'],
                                       password=config['password'],
                                       IGDataPath=config['data_path'])
        self._page = None
        self._followers = list()
        self._current_follower = 0
        self._config = config

        # Login
        self.login()

        # History
        self._histories = {'follow': list(), 'unfollow': list(), 'post': list(), 'comment': list(), 'like': list()}
        self._counts = {'follow': 0, 'unfollow': 0, 'post': 0, 'comment': 0, 'like': 0}

        # Limits
        self._limits = dict()
        self._limits['follow'] = bot_config.friends['max_new_followers']
        self._limits['unfollow'] = bot_config.friends['max_new_unfollow']
        self._limits['post'] = bot_config.post['max_posts']
        self._limits['comment'] = bot_config.post['max_comments']
        self._limits['like'] = bot_config.post['max_likes']
    # end __init__

    ###########################################
    # Public
    ###########################################

    # Get session information
    def session(self):
        """
        Get session information
        :return:
        """
        # Check if file exists
        if os.path.exists(self.session_file):
            return json.load(open(self.session_file, 'r'))
        else:
            return None
        # end if
    # end session

    # Login
    def login(self):
        """
        Login
        :return:
        """
        # Get session information
        session = self.session()

        # Login
        if session is None:
            # Try login
            if self._instagram.login():
                # Session
                save_session = {'token': self._instagram.token,
                                'username_id': self._instagram.username_id,
                                'rank_token': self._instagram.rank_token,
                                'uuid': self._instagram.uuid,
                                'session': self._instagram.s.cookies.get_dict(),
                                'user_agent': self._instagram.USER_AGENT,
                                'device_id': self._instagram.device_id}

                # Save
                json.dump(save_session, open(self.session_file, 'w'))
            # end if
        else:
            self._instagram.token = session['token']
            self._instagram.username_id = session['username_id']
            self._instagram.rank_token = session['rank_token']
            self._instagram.uuid = session['uuid']
            for cookie in session['session'].keys():
                value = session['session'][cookie]
                self._instagram.s.cookies[cookie] = value
            # end for
            self._instagram.USER_AGENT = session['user_agent']
            self._instagram.device_id = session['device_id']
            self._instagram.usLoggedIn = True
        # end if
    # end login

    # Post
    def post(self, media_path, media_caption):
        """
        Post
        :param media_path:
        :param media_caption:
        :return:
        """
        # Log
        logging.getLogger(pystr.LOGGER).info(u"Posting {}".format(media_path))
        self._instagram.uploadPhoto(media_path, media_caption)

        # Inc counter
        self._inc_counter('post')
    # end post

    # Comment
    def comment(self, media_id, comment, media_code):
        """
        Comment a post
        :param media_id: Post's ID
        :param comment: Comment to post
        :return:
        """
        # Log
        logging.getLogger(pystr.LOGGER).info(u"Commenting {} : \"{}\" ({})".format(media_id, comment, media_code))
        self._instagram.comment(mediaId=str(media_id), commentText=comment)

        # Inc count
        self._inc_counter('comment')
    # end comment

    # Like
    def like(self, media_id, media_code):
        """
        Like a post
        :param media_id: Post's ID
        :return:
        """
        # Log
        logging.getLogger(pystr.LOGGER).info(u"Liking {} ({})".format(media_id, media_code))
        self._instagram.like(mediaId=str(media_id))

        # Inc count
        self._inc_counter('comment')
    # end like

    # Follow
    def follow(self, user_id):
        """
        Follow
        :param user_id:
        :return:
        """
        # Log
        logging.getLogger(pystr.LOGGER).info(u"Following {}".format(user_id))
        self._instagram.follow(user_id)

        # Inc count
        self._inc_counter('follow')
    # end follow

    # Unfollow
    def unfollow(self, user_id):
        """
        Unfollow
        :param user_id:
        :return:
        """
        # Log
        logging.getLogger(pystr.LOGGER).info(u"Unfollow {}".format(user_id))

        # Inc count
        self._inc_counter('unfollow')
    # end unfollow

    # Get hashtag feed
    def hashtag_feed(self, hashtag, maxid=''):
        """
        Get hashtag feed
        :param hashtag:
        :param maxid:
        :return:
        """
        return self._instagram.getHashtagFeed(hashtag, maxid)
    # end hashtag_feed

    # Get username info
    def username_info(self, username_id):
        """
        Get username info
        :param username_id:
        :return:
        """
        return self._instagram.getUsernameInfo(username_id)
    # end username_info

    # Get followers
    def followers(self):
        """
        Get followers
        :return:
        """
        return self._instagram.getTotalSelfFollowers()
    # end followers

    # Get following
    def following(self):
        """
        Get following
        :return:
        """
        return self._instagram.getTotalSelfFollowing()
    # end following

    ###########################################
    # Override
    ###########################################

    ###########################################
    # Private
    ###########################################

    # Increment counter
    def _inc_counter(self, action_type):
        """
        Increment follow counter
        :return:
        """
        # Add to history
        self._histories[action_type].append(datetime.datetime.utcnow())

        # Last 24h list
        last_day = list()
        last_day_counter = 0
        for action_time in self._histories[action_type]:
            if (datetime.datetime.utcnow() - action_time).total_seconds() <= 60 * 60 * 24:
                last_day.append(action_time)
                last_day_counter += 1
            # end if
        # end for

        # History and counter
        self._histories[action_type] = last_day
        self._counts[action_type] = last_day_counter
    # end _inc_follow_counter

# end InstagramConnector
