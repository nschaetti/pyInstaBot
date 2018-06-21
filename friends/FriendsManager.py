#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : __init__.py
# Description : Main init file.
# Auteur : Nils Schaetti <n.schaetti@gmail.com>
# Date : 11.02.2018 13:51:05
# Lieu : Nyon, Suisse
#
# This file is part of the pyInstaBot.
# The pyInstaBot is a set of free software:
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
# import pyTweetBot.executor
from pyInstaBot.patterns.singleton import singleton
import pyInstaBot.db.obj
from sqlalchemy import update, delete
from sqlalchemy.orm import load_only
from sqlalchemy import and_, not_
import time
import logging
from datetime import timedelta
import pyInstaBot.tools.strings as pystr
import pyInstaBot.db.obj
import pyInstaBot.instagram


##############################################
# EXCEPTION
##############################################


# Exception, Useless action because already done (already following a user)
class ActionAlreadyDone(Exception):
    """
    Exception, useless action because already done (already following a user)
    """
    pass
# end ActionAlreadyDone


##############################################
# CLASS
##############################################


# The class manage followers and following in the database and do
# the links between the DB and the Twitter management part.
@singleton
class FriendsManager(object):
    """
    The class manage followers and following in the database and do
    the links between the DB and the Twitter management part.
    """

    # Constructor
    def __init__(self, instagram):
        """
        Constructor
        """
        # DB session
        self._session = pyInstaBot.db.DBConnector().get_session()

        # Instagram connector
        self._instagram_con = instagram

        # Logger
        self._logger = logging.getLogger(name=pystr.LOGGER)
    # end __init__

    ######################################################
    # PROPERTIES
    ######################################################

    # Get the number of followers
    @property
    def n_followers(self):
        """
        Get the nunber of followers.
        :return: The number of followers.
        """
        return 0
    # end n_followers

    # Get the number of following
    @property
    def n_followings(self):
        """
        Get the number of following.
        :return: The number of following.
        """
        return 0
    # end n_followers

    # Get followers cursor
    @property
    def followers_cursor(self):
        """
        Get followers cursor
        :return: Followers cursor
        """
        return None
    # end followers_cursor

    # Get followers
    @property
    def followers(self):
        """
        Get followers
        :return: A list of Friend objects
        """
        return self._session.query(pyInstaBot.db.obj.User).filter(pyInstaBot.db.obj.User.user_is_follower).all()
    # end get_followers

    # Get following
    @property
    def followings(self):
        """
        Get following
        :return: A list of friend objects
        """
        return self._session.query(pyInstaBot.db.obj.User).filter(pyInstaBot.db.obj.User.user_is_follower).all()
    # end get_following

    ######################################################
    # PUBLIC FUNCTIONS
    ######################################################

    # Is friend a follower?
    def is_follower(self, screen_name):
        """
        Is friend a follower?
        :param screen_name: Friend's screen name
        :return: True or False
        """
        return self._session.query(pyInstaBot.db.obj.User).filter(and_(
            pyInstaBot.db.obj.User.friend_screen_name == screen_name,
            pyInstaBot.db.obj.User.user_is_follower)).count > 0
    # end is_follower

    # Am I following this friend?
    def is_following(self, full_name):
        """
        Am I following this friend?
        :param full_name: Friend's screen name
        :return: True or False
        """
        return self._session.query(pyInstaBot.db.obj.User).filter(
            and_(pyInstaBot.db.obj.User.user_full_name == full_name,
                 pyInstaBot.db.obj.User.user_is_following == 1)).count() > 0
    # end is_following

    # Get obsolete friends
    def get_obsolete_friends(self, days):
        """
        Get obsolete friends
        :param days: Number of days to be obsolete.
        :return: The list of obsolete friends.
        """
        # Transform back to date
        # Limit date
        datetime_limit = datetime.datetime.utcnow() - timedelta(days=days)

        # Get all
        return self._session.query(pyInstaBot.db.obj.User).filter(
            and_(
                pyInstaBot.db.obj.User.user_is_following == True,
                not_(pyInstaBot.db.obj.User.user_is_follower == True),
                pyInstaBot.db.obj.User.user_following_date <= datetime_limit)
        ).all()
    # end get_obsolete_friends

    # Get uncontacted friends
    def get_uncontacted_friends(self):
        """
        Get uncontacted friends
        :return: Uncontacted friends
        """
        # Get all
        return self._session.query(pyInstaBot.db.obj.User).filter\
        (
            and_(
                pyInstaBot.db.obj.User.user_is_following == True,
                pyInstaBot.db.obj.User.friend_contacted == False
            )
        )
    # end get_uncontacted_friends

    # Get a friend from the DB
    def get_friend_by_id(self, user_id):
        """
        Get a friend from the DB.
        :param friend_id: The friend to get as a Tweepy object.
        :return: The friend DB object.
        """
        return self._session.query(pyInstaBot.db.obj.User).filter(pyInstaBot.db.obj.User.user_id == user_id).one()
    # end get_friend_by_id

    # Get a friend from the DB
    def get_friend_by_name(self, user_name):
        """
        Get a friend from the DB.
        :param screen_name: The friend to get as a Tweepy object.
        :return: The friend DB object.
        """
        return self._session.query(pyInstaBot.db.obj.User).filter(
            pyInstaBot.db.obj.User.friend_screen_name == user_name
        ).one()
    # end get_friend_by_name

    # Friend exists
    def exists(self, screen_name):
        """
        Check if we are followed by a Twitter account.
        :param screen_name: Account's screen name
        :return: True or False
        """
        return len(
            self._session.query(pyInstaBot.db.obj.User).filter(
                pyInstaBot.db.obj.User.friend_screen_name == screen_name
            ).all()
        ) > 0
    # end exists

    # Follow a Twitter account
    def follow(self, screen_name):
        """
        Follow a Twitter account
        :param screen_name: User's screen name
        :return: True if followed, False is already followed
        """
        pass
    # end follow

    # Unfollow a Twitter account
    def unfollow(self, screen_name):
        """
        Unfollow a Twitter account
        :param screen_name: User's scree name
        :return: True of False if succeeded
        """
        pass
    # end unfollow

    # Update followers and following
    def update(self):
        """
        Update followers and following
        :return: New follower count, Lost follower count, New following count, Lost following count
        """
        # Update followers
        self._update_follower()

        # Update following
        # self._update_following()
    # end update

    ######################################################
    # PRIVATE FUNCTIONS
    ######################################################

    # Add a user
    def _add_user(self, user):
        """
        Add a user
        :param user:
        :return:
        """
        self._session.add(user)
        self._session.commit()
    # end _add_user

    # Update following
    def _update_following(self):
        """
        Update following
        :return:
        """
        # For each following
        for user in pyInstaBot.instagram.InstagramConnector().following():
            if not pyInstaBot.db.obj.User.exists(user.user_id):
                logging.getLogger(pystr.LOGGER).info(u"New following in the database : {}".format(user))

                # Following
                user.user_is_following = True
                user.user_following_date = datetime.datetime.utcnow()

                # Add
                self._add_user(user)
            elif not pyInstaBot.db.obj.User.get(user.user_id).is_following():
                # Update
                user.user_is_following = True
                user.user_following_date = datetime.datetime.utcnow()
            # end if
        # end for
    # end _update_follower

    # Update follower
    def _update_follower(self):
        """
        Update follower
        :return:
        """
        # For each follower
        for user in pyInstaBot.instagram.InstagramConnector().followers():
            if not pyInstaBot.db.obj.User.exists(user['username']):
                # Log
                logging.getLogger(pystr.LOGGER).info(u"New follower in the database : {}".format(user['username']))

                # User info
                info = pyInstaBot.instagram.InstagramConnector().username_info(user['pk'])

                # New user
                new_user = pyInstaBot.db.obj.User(
                    user_username=user['username'],
                    user_full_name=user['full_name'],
                    user_biography=info['user']['biography'],
                    user_profile_pic_url=user['profile_pic_url'],
                    user_is_verified=user['is_verified'],
                    user_is_follower=True,
                    user_follower_date=datetime.datetime.now()
                )

                # Add
                self._add_user(new_user)
            elif not pyInstaBot.db.obj.User.get(user['username']).user_is_follower:
                # Update
                user.user_is_follower = True
                user.user_follower_date = datetime.datetime.now()
            # end if
        # end for
    # end _update_following

# end FriendsManager
