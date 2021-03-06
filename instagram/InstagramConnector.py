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
from pyInstaBot.InstagramAPI import InstagramAPI
import os
import json
import time


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
        self._queries = 0

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
            self._instagram.isLoggedIn = True
        # end if
    # end login

    # Post
    def post(self, media_path, media_caption, media_thumbnail="", media_location=""):
        """
        Post
        :param media_path: Media's path
        :param media_caption: Media's caption
        :return: True if ok, False if error
        """
        # Log
        logging.getLogger(pystr.LOGGER).info(u"Posting {}".format(media_path))

        # Location
        if media_location == "" or media_location is None:
            location = None
        else:
            location = self.get_location(media_location)['location']
        # end if

        # Success
        success = False

        # Tries
        for i in range(5):
            # Check file
            if ".jpg" in media_path or ".jpeg" in media_path or ".png" in media_path:
                self._instagram.uploadPhoto(media_path, media_caption, location=location)
                response = self._instagram.LastResponse
            elif ".mp4" in media_path:
                self._instagram.uploadVideo(media_path, media_thumbnail, media_caption)
                response = self._instagram.LastResponse
            elif type(media_path) is list:
                self._instagram.uploadAlbum(media_path, media_caption)
                response = self._instagram.LastResponse
            else:
                logging.getLogger(pystr.LOGGER).info(u"Invalid media type {}".format(media_path))
                return False
            # end if

            # Check response
            if response.status_code == 200:
                success = True
                break
            # end if

            # Sleep
            logging.getLogger(pystr.LOGGER).info(u"Post failed, waiting 15 seconds to retry...")
            time.sleep(15)
        # end for

        # Inc counter
        self._inc_queries()
        self._inc_counter('post')

        return success
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

        # Check response
        if self._instagram.LastResponse.status_code != 200:
            return False
        # end if

        # Inc count
        self._inc_queries()
        self._inc_counter('comment')

        return True
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

        # Check response
        if self._instagram.LastResponse.status_code != 200:
            return False
        # end if

        # Inc count
        self._inc_queries()
        self._inc_counter('comment')

        return True
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

        # Check response
        if self._instagram.LastResponse.status_code != 200:
            return False
        # end if

        # Inc count
        self._inc_queries()
        self._inc_counter('follow')

        return True
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
        self._instagram.unfollow(user_id)

        # Check response
        if self._instagram.LastResponse.status_code != 200:
            return False
        # end if

        # Inc count
        self._inc_queries()
        self._inc_counter('unfollow')

        return True
    # end unfollow

    # Get hashtag feed
    def hashtag_feed(self, hashtag, maxid=''):
        """
        Get hashtag feed
        :param hashtag:
        :param maxid:
        :return:
        """
        # Counters
        self._inc_queries()

        # Try
        try:
            response = self._instagram.getHashtagFeed(hashtag, maxid)
        except ValueError:
            return False
        # end try

        if response:
            return self._instagram.LastJson
        else:
            return False
        # end if
    # end hashtag_feed

    # Get username info
    def username_info(self, username_id):
        """
        Get username info
        :param username_id:
        :return:
        """
        self._inc_queries()
        if self._instagram.getUsernameInfo(username_id):
            return self._instagram.LastJson
        else:
            return False
        # end if
    # end username_info

    # Search username
    def search_username(self, username):
        """
        Search username
        :param username:
        :return:
        """
        self._inc_queries()
        if self._instagram.searchUsername(username):
            return self._instagram.LastJson
        else:
            return False
        # end if
    # end search_username

    # Get followers
    def followers(self):
        """
        Get followers
        :return:
        """
        self._inc_queries()
        return self._instagram.getTotalSelfFollowers()
    # end followers

    # Get following
    def following(self):
        """
        Get following
        :return:
        """
        self._inc_queries()
        return self._instagram.getTotalSelfFollowings()
    # end following

    # Media info
    def media_info(self, media_id):
        """
        Media info
        :param media_id:
        :return:
        """
        self._inc_queries()
        if self._instagram.mediaInfo(media_id):
            return self._instagram.LastJson
        else:
            return False
        # end if
    # end media_info

    # Search locations
    def search_location(self, query):
        """
        Search locations
        :param query:
        :return:
        """
        self._inc_queries()
        if self._instagram.searchLocation(query):
            return self._instagram.LastJson
        else:
            return False
        # end if
    # end search_locations

    # Get location
    def get_location(self, location):
        """
        Get location
        :param location:
        :return:
        """
        self._inc_queries()
        if self._instagram.searchLocation(location):
            return self._instagram.LastJson['items'][0]
        else:
            return False
        # end if
    # end get_location

    # Get timeline
    def timeline(self):
        """
        Timeline
        :return:
        """
        self._inc_queries()
        if self._instagram.getTimeline():
            return self._instagram.LastJson
        else:
            return False
        # end if
    # end timeline

    # Get user feed
    def user_feed(self, max_id=''):
        """
        Get user feed
        :return:
        """
        self._inc_queries()
        if self._instagram.getUserFeed(usernameId=self._config['user_id'], maxid=max_id):
            return self._instagram.LastJson
        else:
            return False
        # end if
    # end user_feed

    ###########################################
    # Override
    ###########################################

    ###########################################
    # Private
    ###########################################

    # Wait
    def _wait(self):
        """
        Wait
        :return:
        """
        logging.getLogger(pystr.LOGGER).info(u"Waiting 60 seconds...")
        time.sleep(60)
    # end _wait

    # Increment queries
    def _inc_queries(self):
        """
        Increment queries
        :return:
        """
        # Increment
        self._queries += 1

        # Wait
        if self._queries % 15 == 0:
            self._wait()
        # end if
    # end _inc_queries

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
