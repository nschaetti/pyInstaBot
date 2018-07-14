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
from sqlalchemy import Column, BigInteger, Boolean, Unicode, DateTime, and_
from .Base import Base
import pyInstaBot.tools.strings as pystr
import logging


# Comment
class Comment(Base):
    """
    Comment
    """

    # Table name
    __tablename__ = "pyinstb_comments"

    # Fields
    comment_id = Column(BigInteger, primary_key=True)
    comment_text = Column(Unicode(500), nullable=False)
    comment_username = Column(Unicode(100), nullable=False)
    comment_media = Column(BigInteger, nullable=False)
    comment_date = Column(DateTime, nullable=False, default=None)

    ############################################
    # Public
    ############################################

    ############################################
    # Override
    ############################################

    # Exists for username
    @staticmethod
    def exists_username(comment_text, comment_username):
        """
        Exists
        :param user_username:
        :return:
        """
        return pyInstaBot.db.DBConnector().get_session().query(Comment).filter(
            and_(
                Comment.comment_text == comment_text,
                Comment.comment_username == comment_username
            )).count() > 0
    # end exists

    # Exists for media
    @staticmethod
    def exists_media(comment_media):
        """
        Exists for media
        :param comment_media:
        :return:
        """
        return pyInstaBot.db.DBConnector().get_session().query(Comment).filter(
            Comment.comment_media == comment_media
        ).count() > 0
    # end exists_media

    # Get user
    @staticmethod
    def get_for_user(user_username):
        """
        Get user
        :param user_username:
        :return:
        """
        return pyInstaBot.db.DBConnector().get_session().query(Comment).filter(
            Comment.comment_username == user_username
        ).all()
    # end get

    # Get
    @staticmethod
    def get(comment_text):
        """
        Get for comment
        :param comment_text:
        :return:
        """
        return pyInstaBot.db.DBConnector().get_session().query(Comment).filter(
            Comment.comment_text == comment_text
        ).all()
    # end get

    # Add
    @staticmethod
    def add(media_id, comment_username, comment_text):
        """
        Add
        :param media_id:
        :param comment_username:
        :param comment_text:
        :return:
        """
        # New comment
        comment = Comment(
            comment_text=comment_text,
            comment_username=comment_username,
            comment_media=media_id,
            comment_date=datetime.datetime.utcnow()
        )

        # Log
        logging.getLogger(pystr.LOGGER).info(
            u"New comment \"{}\" for media {} and user {} added to the database".format(
                comment_username,
                media_id,
                comment_username
            )
        )

        # Commit
        pyInstaBot.db.DBConnector().get_session().add(comment)
        pyInstaBot.db.DBConnector().get_session().commit()
    # end add

    ############################################
    # Override Functions
    ############################################

# end User
