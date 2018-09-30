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


# Statistic
class Statistic(Base):
    """
    Statistic
    """

    # Table name
    __tablename__ = "pyinstb_statistics"

    # Fields
    statistic_id = Column(BigInteger, primary_key=True)
    statistic_followers_count = Column(BigInteger, nullable=False, default=0)
    statistic_followings_count = Column(BigInteger, nullable=False, default=0)
    statistic_likes_count = Column(BigInteger, nullable=False, default=0)
    statistic_comments_count = Column(BigInteger, nullable=False, default=0)
    statistic_date = Column(DateTime, nullable=False, default=datetime.datetime.now())

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
