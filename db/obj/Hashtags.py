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
from sqlalchemy import Column, BigInteger, Boolean, Unicode, DateTime, and_, Float, Table, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import PrimaryKeyConstraint
from .Base import Base
import pyInstaBot.tools.strings as pystr
import logging


HashtagLink = Table(
    'pyinstb_hashtag_link',
    Base.metadata,
    Column('hashtaglink_id', BigInteger, primary_key=True),
    Column('hashtaglink_hashtag1', BigInteger, ForeignKey('pyinstb_hashtags.hashtag_id'), primary_key=True),
    Column('hashtaglink_hashtag2', BigInteger, ForeignKey('pyinstb_hashtags.hashtag_id'), primary_key=True),
    Column('hashtaglink_count', Integer, nullable=False, default=0)
)


# Hashtag link
"""class HashtagLink(Base):
    
    Hashtag link
    

    # Table name
    __tablename__ = "pyinstb_hashtag_link"

    # Fields
    hashtaglink_id = Column('hashtaglink_id', BigInteger, primary_key=True)
    hashtaglink_hashtag1 = Column('hashtaglink_hashtag1', BigInteger, ForeignKey('pyinstb_hashtags.hashtag_id'), primary_key=True),
    hashtaglink_hashtag2 = Column('hashtaglink_hashtag2', BigInteger, ForeignKey('pyinstb_hashtags.hashtag_id'), primary_key=True),
    hashtaglink_count = Column('hashtaglink_count', Integer, default=0)

# end HashtagLink"""


# Hashtags
class Hashtags(Base):
    """
    Hashtags
    """

    # Table name
    __tablename__ = "pyinstb_hashtags"

    # Fields
    hashtag_id = Column(BigInteger, primary_key=True)
    hashtag_text = Column(Unicode(500), nullable=False)
    hashtag_engagement_rate = Column(Float, nullable=False, default=0.0)
    hashtag_count = Column(BigInteger, nullable=False, default=0)
    hashtag_link = relationship(
        'Hashtags',
        secondary=HashtagLink,
        primaryjoin=hashtag_id == HashtagLink.c.hashtaglink_hashtag1,
        secondaryjoin=hashtag_id == HashtagLink.c.hashtaglink_hashtag2
    )

    ############################################
    # Public
    ############################################

    ############################################
    # Override
    ############################################

    ############################################
    # Override Functions
    ############################################

# end User
