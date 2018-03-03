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

# Default configuration
default_config = \
{
    "instagram" :
    {
        "user_id": {},
        "username": {},
        "password": {}
    },
	"scheduler" :
	{
		"sleep": [6, 13]
	},
	"hashtags":
	[
	],
	"friends" :
	{
		"max_new_followers" : 40,
		"max_new_unfollow" : 40,
		"interval" : [30, 45],
		"ratio" : 0.8
	},
	"forbidden_words" :
	[
	],
	"post" :
	{
		"post_interval": [30, 90],
		"like_interval": [0, 4],
		"comment_interval": [0, 8],
        "max_posts": 24,
        "max_likes": 500,
        "max_comments": 500,
		"languages": ["en", "fr"]
	}
}
