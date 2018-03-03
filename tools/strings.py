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


# Logger's name
LOGGER = u"pyInstaBot"

#########################################
# ERRORS
#########################################

# Parsing configuration file
ERROR_PARSING_CONFIG_FILE = u"Error parsing configuration file : {}\n"

# Unknown command
ERROR_UNKNOWN_COMMAND = u"Unknown command {}\n"

# Reservoir full
ERROR_RESERVOIR_FULL = u"Reservoir full for Tweet action, exiting..."

# Comment/like already in DB
ERROR_COMMENT_ALREADY_DB = u"Comment \"{}\" already exists in the database"
ERROR_LIKE_ALREADY_DB = u"Like \"{}\" already exists in the database"

##########################################
# INFO
##########################################

# Adding like/comment to DB
INFO_ADD_COMMENT_SCHEDULER = u"Adding comment \"{}\" for media {} to the scheduler"
INFO_ADD_LIKE_SCHEDULER = u"Adding like for media {} to the scheduler"

# ALSEEP
INFO_ASLEEP = u"I'm asleep!"

############################################
# DEBUG
############################################

DEBUG_NEW_MEDIA_FOUND = u"New media found for hashtag {} : {}\n"
