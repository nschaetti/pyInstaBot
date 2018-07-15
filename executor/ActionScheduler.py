#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : executor/ActionScheduler.py
# Description : Manage bot's actions.
# Auteur : Nils Schaetti <n.schaetti@gmail.com>
# Date : 15.06.2017 18:14:00
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

import sqlalchemy
import datetime
from datetime import timedelta
import pyInstaBot
import pyInstaBot.db
import pyInstaBot.db.obj
from sqlalchemy import and_
import logging
from pyInstaBot.patterns.singleton import singleton
import random
import sys
import pyInstaBot.tools.strings as pystr


# Reservoir full exception
class ActionReservoirFullError(Exception):
    """
    Reservoir is full
    """
    pass
# end ActionReservoirFullError


# Action already in the DB
class ActionAlreadyExists(Exception):
    """
    The action is already registered in the DB
    """
    pass
# end ActionAlreadyExists


# No factory set
class NoFactory(Exception):
    """
    No factory to create Tweets
    """
    pass
# end NoFactory


# Manage bot's action
@singleton
class ActionScheduler(object):
    """
    Manage bot's action
    """

    # Properties
    action_types = ["Post", "Comment", "Like", "Follow", "Unfollow"]

    # Constructor
    def __init__(self, config, update_delay=timedelta(minutes=10), reservoir_size=timedelta(days=3),
                 purge_delay=timedelta(weeks=2)):
        """
        Constructor
        :param config:
        :param n_actions:
        :param update_delay:
        :param reservoir_size:
        :param purge_delay:
        :param stats:
        """
        # Properties
        self._session = pyInstaBot.db.DBConnector().get_session()

        self._purge_delay = purge_delay
        self._reservoir_size = reservoir_size
        self._update_delay = update_delay
        self._config = config

        # Purge the reservoir
        self._purge_reservoir()
    # end __init__

    ##############################################
    # Public
    ##############################################

    # Add an action to the DB
    def add(self, action, generate_order=False):
        """
        Add an action to the DB
        :param action:
        :return:
        """
        # Generate order
        if generate_order:
            action.action_order = self._generate_random_order()
        # end if

        # Check that the reservoir is not full
        if not self.full(action.action_type):
            # Add action
            self._session.add(action)

            # Commit
            self._session.commit()
        else:
            raise ActionReservoirFullError(u"To many action in the reservoir to add a new one")
        # end if
    # end add

    # Add a follow action in the DB
    def add_follow(self, user_id):
        """
        Add a "follow" action in the DB:
        :param friend_id:
        :return:
        """
        if not self.exists_friend_action(action_type="Follow", action_post_id=user_id):
            # Insert
            new_action = pyInstaBot.db.obj.Action(action_type='Follow', action_order=self._generate_random_order(),
                                                  action_post_id=user_id)
            logging.getLogger(pystr.LOGGER).info(u"New follow {} action add to the database".format(user_id))
            self._session.add(new_action)
            self._session.commit()
        else:
            raise ActionAlreadyExists(
                u"Follow action for user id {} already in database".format(user_id))
        # end if
    # end add_follow

    # Add an unfollow action in the DB
    def add_unfollow(self, user_id):
        """
        Add an "unfollow" action in the DB:
        :param friend_id: Twitter account0's ID.
        """
        if not self.exists(action_type="Unfollow", action_post_id=user_id):
            # Insert
            new_action = pyInstaBot.db.obj.Action(action_type='Unfollow', action_order=self._generate_random_order(),
                                                  action_tweet_text=user_id)
            logging.getLogger(pystr.LOGGER).info(u"New unfollow {} action add to the database".format(user_id))
            self._session.add(new_action)
            self._session.commit()
        else:
            raise ActionAlreadyExists(
                u"Unfollow action for screen name {} already in database".format(user_id))
        # end if
    # end add_unfollow

    # Add a like action in the DB
    def add_like(self, media_id, media_code):
        """
        Add a "like" action in the DB.
        :param media_id: Media's ID
        """
        if not self.exists_like_action(action_post_id=media_id):
            action = pyInstaBot.db.obj.Action(action_type='Like', action_order=self._generate_random_order(),
                                              action_post_id=media_id, action_post_image=media_code)
            logging.getLogger(pystr.LOGGER).info(
                u"New like {} ({}) action add to the database".format(media_id, media_code))
            self._session.add(action)
            self._session.commit()
        else:
            logging.getLogger(pystr.LOGGER).warning(u"Like action for media {} ({}) already in database"
                                                    .format(media_id, media_code))
            raise ActionAlreadyExists(u"Like action for media {} ({}) already in database".format(media_id, media_code))
        # end if
    # end add_like

    # Add a post action in the DB
    def add_post(self, media_path, media_thumbnail, media_caption, media_location=None, action_loop=False, action_filter="none"):
        """
        Add a post action in the DB
        :param media_path:
        :param media_caption:
        :return:
        """
        if not self.exists_post_action(action_post_image=media_path, action_post_text=media_caption):
            action = pyInstaBot.db.obj.Action(
                action_type='Post',
                action_order=self._generate_random_order(),
                action_post_image=media_path,
                action_post_text=media_caption,
                action_post_thumbnail=media_thumbnail,
                action_post_location=media_location,
                action_post_filter=action_filter,
                action_loop=action_loop,
            )
            logging.getLogger(pystr.LOGGER).info(u"New post {} action add to the database".format(media_path.decode('utf-8')))
            self._session.add(action)
            self._session.commit()
        else:
            logging.getLogger(pystr.LOGGER).warning(u"Post action for media {} already in database"
                                                    .format(media_path))
            raise ActionAlreadyExists(u"Post action for media {} already in database".format(media_path))
        # end if
    # end add_tweet

    # Add a "Comment" action in the DB
    def add_comment(self, media_id, comment_text, media_code, comment_username):
        """
        Add a "Comment" action in the DB
        :param media_id:
        :param comment_text:
        :return:
        """
        if not self.exists_comment_action(action_post_id=media_id):
            action = pyInstaBot.db.obj.Action(
                action_type='Comment',
                action_order=self._generate_random_order(),
                action_post_id=media_id,
                action_post_text=comment_text,
                action_post_image=media_code,
                action_post_username=comment_username
            )
            logging.getLogger(pystr.LOGGER).info(
                u"New comment {} ({}) action add to the database".format(media_id, media_code))
            self._session.add(action)
            self._session.commit()
        else:
            logging.getLogger(pystr.LOGGER).warning(u"Comment action for media {} ({}) already in database"
                                                    .format(media_id, media_code))
            raise ActionAlreadyExists(u"Post action for media {} ({}) already in database".format(media_id, media_code))
        # end if
    # end add_comment

    # Does a follow/unfollow already exists in the DB?
    def exists_friend_action(self, action_type, action_post_id):
        """
        Does a follow/unfollow already exists in the DB?
        :param action_type:
        :param action_post_id:
        :return:
        """
        try:
            self._session.query(pyInstaBot.db.obj.Action).filter(
                and_(pyInstaBot.db.obj.Action.action_type == action_type, pyInstaBot.db.obj.Action.action_post_id == action_post_id)).one()
            return True
        except sqlalchemy.orm.exc.NoResultFound:
            return False
        # end try
    # end exists

    # Does a like action already exists in the DB?
    def exists_like_action(self, action_post_id):
        """
        Does a like action already exists in the DB?
        :param action_post_id:
        :return:
        """
        try:
            self._session.query(pyInstaBot.db.obj.Action).filter(
                and_(pyInstaBot.db.obj.Action.action_type == 'Like',
                     pyInstaBot.db.obj.Action.action_post_id == action_post_id)).one()
            return True
        except sqlalchemy.orm.exc.NoResultFound:
            return False
        # end try
    # end exists

    # Does a post action already exists in the DB?
    def exists_post_action(self, action_post_image, action_post_text):
        """
        Does a post action already exists in the DB?
        :param action_post_image:
        :param action_post_text:
        :return:
        """
        try:
            self._session.query(pyInstaBot.db.obj.Action).filter(
                and_(pyInstaBot.db.obj.Action.action_type == 'Post',
                     pyInstaBot.db.obj.Action.action_post_image == action_post_image,
                     pyInstaBot.db.obj.Action.action_post_text == action_post_text)).one()
            return True
        except sqlalchemy.orm.exc.NoResultFound:
            return False
        # end try
    # end exists

    # Does a comment action already exists in the DB?
    def exists_comment_action(self, action_post_id):
        """
        Does a comment action already exists in the DB?
        :param action_post_id:
        :return:
        """
        try:
            self._session.query(pyInstaBot.db.obj.Action).filter(
                and_(pyInstaBot.db.obj.Action.action_type == 'Comment',
                     pyInstaBot.db.obj.Action.action_post_id == action_post_id)).one()
            return True
        except sqlalchemy.orm.exc.NoResultFound:
            return False
        # end try
    # end exists

    # Delete an action
    def delete(self, action):
        """
        Delete an action
        :param action: Action to delete.
        """
        self._session.query(pyInstaBot.db.obj.Action).filter(pyInstaBot.db.obj.Action.action_id == action.action_id).delete()
        self._session.commit()
    # end delete

    # Execute next actions
    def exec_next_actions(self):
        """
        Execute next actions
        :return:
        """
        for action_type in self.action_types:
            # Get action to be executed
            self.exec_next_action(action_type=action_type)
        # end for
    # end exec_next_action

    # Execute next action (by type)
    def exec_next_action(self, action_type):
        """
        Execute next action (by type)
        :param action_type: Action's type (like, follow, etc)
        :return:
        """
        # Get all actions
        action = self._session.query(pyInstaBot.db.obj.Action).filter(pyInstaBot.db.obj.Action.action_type == action_type) \
            .order_by(pyInstaBot.db.obj.Action.action_id).all()[0]
        action.execute()
        self.delete(action)
    # end exec_next_action

    # Next action
    def next_action_to_execute(self, action_type):
        """
        Get next action to execute
        :param action_type:
        :return:
        """
        return self._get_exec_action(action_type)
    # end next_action_to_execute

    # List actions in the reservoir
    def list_actions(self, action_type=""):
        """
        List actions in the reservoir
        :return:
        """
        # Get actions
        if action_type == "":
            return self._session.query(pyInstaBot.db.obj.Action).order_by(pyInstaBot.db.obj.Action.action_id).all()
        else:
            return self._session.query(pyInstaBot.db.obj.Action).filter(pyInstaBot.db.obj.Action.action_type == action_type).order_by(pyInstaBot.db.obj.Action.action_id).all()
        # end if
    # end list_actions

    # Is reservoir empty
    def empty(self, action_type):
        """
        Is the reservoir empty?
        :param action_type: Action type
        :return: True or False
        """
        return self._get_reservoir_level(action_type) == 0
    # end if

    # Check if the actions reservoir is full.
    def full(self, action_type):
        """
        Check if the actions reservoir is full for this
        kind of action.
        :param action_type: The kind of action
        :return:
        """
        # Get reservoir level
        reservoir_level = self._get_reservoir_level(action_type)

        # Get interval
        if action_type == "Tweet":
            (min_time, max_time) = self._config.tweet['interval']
        elif action_type == "Retweet" or action_type == "Like":
            (min_time, max_time) = self._config.retweet['interval']
        elif action_type == "Follow" or action_type == "Unfollow":
            (min_time, max_time) = self._config.friends['interval']
        # end if

        # Average
        average_time = (min_time + max_time) / 2.0

        # Max number of actions
        max_n_action = int(self._reservoir_size.total_seconds() / (average_time * 60))

        # Log
        logging.debug(u"is_reservoir_full: {} in the reservoir for a max value of {}".format(reservoir_level,
                                                                                            max_n_action))

        # reservoir_level >= max_n_action => full
        return reservoir_level >= max_n_action
    # end _is_reservoir_full

    # Get the number of statuses
    def n_statuses(self):
        """
        Get the number of statuses
        :return: The number of statuses
        """
        return pyInstaBot.twitter.TweetBotConnector().get_user().statuses_count
    # end n_statuses

    ##############################################
    # Private functions
    ##############################################

    # Generate random order
    def _generate_random_order(self):
        """
        Generate random order
        :return:
        """
        return random.randint(0, sys.maxint)
    # end _generate_random_order

    # Purge reservoir
    def _purge_reservoir(self):
        """
        Purge the reservoir of obsolete actions.
        """
        self._session.query(pyInstaBot.db.obj.Action).filter(pyInstaBot.db.obj.Action.action_date <= datetime.datetime.utcnow() - self._purge_delay)
    # end _purge_reservoir

    # Get reservoir levels
    def _get_reservoir_levels(self):
        """
        Get the number of actions in the reservoir.
        :return: The number of action as a dict()
        """
        result = dict()
        # Level per action
        for action_type in self.action_types:
            result[action_type] = self._get_reservoir_level(action_type)
        # end for
        return result
    # end _get_reservoir_level

    # Get reservoir level
    def _get_reservoir_level(self, action_type):
        """
        Get the number of action for a action type.
        :param action_type: Action's type.
        :return: Reservoir level for this action
        """
        return len(self._session.query(pyInstaBot.db.obj.Action).filter(pyInstaBot.db.obj.Action.action_type == action_type).all())
    # end _get_reservoir_level

    # Get action to execute
    def _get_exec_action(self, action_type):
        """
        Get all action to execute
        :return: Action to execute as a list()
        """
        # Get all actions
        exec_actions = self._session.query(pyInstaBot.db.obj.Action).filter(
            and_(pyInstaBot.db.obj.Action.action_type == action_type,
                 pyInstaBot.db.obj.Action.action_executed == False)).order_by(
            pyInstaBot.db.obj.Action.action_order).all()

        # Log debug
        logging.getLogger(pystr.LOGGER).debug(u"_get_exec_action : {}".format(exec_actions))

        return exec_actions[0] if len(exec_actions) > 0 else None
    # end _get_exec_action

    # Add action with id
    def _add_id_action(self, action_type, the_id):
        """
        Add action with a id argument.
        :param action_type: Type of action
        :param the_id: Action's ID
        """
        if not self.exists(action_type, the_id):
            action = pyInstaBot.db.obj.Action(action_type=action_type, action_order=self._generate_random_order(),
                                   action_tweet_id=the_id)
            self.add(action)
        else:
            logging.getLogger(pystr.LOGGER).warning(u"{} action for friend/tweet {} already in database"
                                                    .format(action_type, the_id))
            raise ActionAlreadyExists(u"{} action for friend/tweet {} already in database".format(action_type, the_id))
        # end if
    # end _add_id_action

    # Add action with text
    def _add_text_action(self, action_type, the_text):
        """
        Add action with text.
        :param action_type: Type of action
        :param the_text: Action's text.
        """
        if not self.exists(action_type=action_type, action_tweet_text=the_text):
            action = pyInstaBot.db.obj.Action(action_type=action_type, action_order=self._generate_random_order(),
                                   action_tweet_text=the_text)
            self.add(action)
        else:
            logging.getLogger(pystr.LOGGER).warning(u"{} action for text {} already in database"
                                                    .format(action_type, the_text))
            raise ActionAlreadyExists(u"{} action for text {} already in database".format(action_type, the_text))
        # end if
    # end _add_text_action

    # Add action with text and ID
    def _add_action(self, action_type, the_id, the_text):
        """
        Add action with text and ID
        :param action_type:
        :param the_id:
        :param the_text:
        :return:
        """
        if not self.exists(action_type=action_type, action_tweet_id=the_id, action_tweet_text=the_text):
            action = pyInstaBot.db.obj.Action(action_type=action_type, action_order=self._generate_random_order(),
                                   action_tweet_id=the_id, action_tweet_text=the_text)
            self.add(action)
        else:
            logging.getLogger(pystr.LOGGER).warning(u"{} action for id {} and text {} already in database"
                                                     .format(action_type, the_id, the_text))
            raise ActionAlreadyExists(
                u"{} action for id {} and text {} already in database".format(action_type, the_id, the_text))
        # end if
    # end _add_action

# end ActionScheduler
