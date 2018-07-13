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
import pyInstaBot
import pyInstaBot.instagram
import datetime
from sqlalchemy import Column, String, BigInteger, DateTime, Enum, Boolean
from .Base import Base
from sqlalchemy import update
from sqlalchemy import and_
import pyInstaBot.db


# Action
class Action(Base):
    """
    Action
    """

    # Table name
    __tablename__ = "pyinstb_actions"

    # Fields
    action_id = Column(BigInteger, primary_key=True)
    action_type = Column(Enum('Post', 'Comment', 'Like', 'Follow', 'Unfollow'), nullable=False)
    action_order = Column(BigInteger, nullable=False)
    action_post_id = Column(BigInteger, nullable=True)
    action_post_text = Column(String(5000), nullable=True)
    action_post_image = Column(String(500), nullable=True)
    action_post_thumbnail = Column(String(500), nullable=True)
    action_loop = Column(Boolean, default=False)
    action_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    action_executed = Column(Boolean, nullable=False, default=False)

    ############################################
    # Public Functions
    ############################################

    # Execute the action
    def execute(self):
        """
        Execute the action
        :return:
        """
        if self.action_type == "Follow":
            # Follow
            response = pyInstaBot.instagram.InstagramConnector().follow(str(self.action_post_id))
        elif self.action_type == "Unfollow":
            # Unfollow
            response = pyInstaBot.instagram.InstagramConnector().unfollow(str(self.action_post_id))
        elif self.action_type == "Like":
            # Like
            response = pyInstaBot.instagram.InstagramConnector().like(self.action_post_id, self.action_post_image)
        elif self.action_type == "Post":
            # Post
            response = pyInstaBot.instagram.InstagramConnector().post(self.action_post_image, self.action_post_text,
                                                                      self.action_post_thumbnail)
        elif self.action_type == "Comment":
            # Comment
            response = pyInstaBot.instagram.InstagramConnector().comment(self.action_post_id, self.action_post_text,
                                                              self.action_post_image)
        # end if

        # Set executed
        self.action_executed = True
        pyInstaBot.db.DBConnector().get_session().commit()

        return response
    # end

    ############################################
    # Static functions
    ############################################

    # To string
    def __str__(self):
        """
        To string
        :return:
        """
        return "Action(id={}, type={}, post_id={}, post_text={}, post_image={}, date={})".format(
            self.action_id,
            self.action_type,
            self.action_post_id,
            self.action_post_text,
            self.action_post_image,
            self.action_date)
    # end __str__

    # To unicode
    def __unicode__(self):
        """
        To unicode
        :return:
        """
        return u"Action(id={}, type={}, post_id={}, post_text={}, post_image={}, date={})".format(
            self.action_id,
            self.action_type,
            self.action_post_id,
            self.action_post_text,
            self.action_post_image,
            self.action_date)
    # end __unicode__

# end Action
