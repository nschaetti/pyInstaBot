#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : Action.py
# Description : pyTweetBot Action in the DB.
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

# Import
import datetime
import pyInstaBot.db
from sqlalchemy import Column, BigInteger, Boolean, Unicode, DateTime
from .Base import Base


# Instagram User
class User(Base):
    """
    Action
    """

    # Table name
    __tablename__ = "pyinstb_users"

    # Fields
    user_id = Column(BigInteger, primary_key=True)
    user_username = Column(Unicode(500), nullable=False)
    user_full_name = Column(Unicode(2000), nullable=False)
    user_biography = Column(Unicode(5000), nullable=True)
    user_profile_pic_url = Column(Unicode(5000), nullable=False)
    user_is_verified = Column(Boolean, nullable=False)
    user_is_follower = Column(Boolean, nullable=True, default=False)
    user_is_following = Column(Boolean, nullable=True, default=False)
    user_follower_date = Column(DateTime, nullable=True, default=None)
    user_following_date = Column(DateTime, nullable=True, default=None)

    ############################################
    # Public
    ############################################

    ############################################
    # Override
    ############################################

    # Exists
    @staticmethod
    def exists(user_username):
        """
        Exists
        :param user_username:
        :return:
        """
        print(user_username)
        print(pyInstaBot.db.DBConnector().get_session().query(User).filter(user_username == user_username).count())
        return pyInstaBot.db.DBConnector().get_session().query(User).filter(User.user_username == user_username).count() > 0
    # end exists

    # Is follower
    @staticmethod
    def is_follower(user_id):
        """
        Is follower?
        :param user_id:
        :return:
        """
        if not User.exists(user_id):
            return False
        else:
            user = User.get(user_id)
            return user.user_is_follower
        # end if
    # end is_follower

    # Is following
    @staticmethod
    def is_following(user_id):
        """
        Is following?
        :param user_id:
        :return:
        """
        if not User.exists(user_id):
            return False
        else:
            user = User.get(user_id)
            return user.user_is_following
            # end if
    # end is_following

    # Get user
    @staticmethod
    def get(user_username):
        """
        Get user
        :param user_username:
        :return:
        """
        return pyInstaBot.db.DBConnector().get_session().query(User).filter(user_username == user_username).all()[0]
    # end get

    ############################################
    # Override Functions
    ############################################

    # To unicode
    def __unicode__(self):
        """
        To unicode
        :return:
        """
        return u"(user_id={},  username={}, full_name={}, pic_url={}, " \
               u"is_verified={}, followed_by_viewer={}, requested_by_viewer={}, "\
               u"is_follower={}, is_following={}, follower_date={}, following_date={})".\
            format(self.user_id, self.user_username, self.user_full_name, self.user_profile_pic_url,
                   self.user_is_verified, self.user_followed_by_viewer, self.user_requested_by_viewer,
                   self.user_is_follower, self.user_is_following, self.user_follower_date,
                   self.user_following_date)
    # end __unicode__

    # To string
    def __str__(self):
        """
        To unicode
        :return:
        """
        return "(user_id={},  username={}, full_name={}, pic_url={}, " \
               "is_verified={}, followed_by_viewer={}, requested_by_viewer={})" \
               "is_follower={}, is_following={}, follower_date={}, following_date={})".\
            format(self.user_id, self.user_username, self.user_full_name.encode('utf-8', errors='ignore'),
                   self.user_profile_pic_url,
                   self.user_is_verified, self.user_followed_by_viewer, self.user_requested_by_viewer,
                   self.user_is_follower, self.user_is_following, self.user_follower_date,
                   self.user_following_date)
    # end __str__

# end User
