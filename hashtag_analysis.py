#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : pyTweetBot.py
# Description : pyTweetBot main execution file.
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
import os
import logging
from moviepy.editor import *
import tools.strings as pystr
import tools.medias as med
import executor.ActionScheduler
import hashtags
import re
import codecs


# Advisable hashtags
def get_advisable_hashtags(hashtag_manager, hashtag_str):
    """
    Advisable hashtags
    :param hashtags:
    :return:
    """
    # Split
    hashtags_list = hashtag_str.split(u",")

    # Get advisable hashtags
    print(hashtag_manager.advisable_hashtags(hashtags_list))
# end get_advisable_hashtags


# Analyse hastag
def analyse_hashtags(hashtag_text):
    """
    Analyse hashtag
    :param hashtag_manager:
    :param hashtag_text:
    :return:
    """
    # Hashtag manager
    hashtag_manager = hashtags.HashtagManager()

    results = hashtag_manager.interest_hashtags([hashtag_text])

    for (n, r, m) in results:
        print(u"Node {}, count {}, relatedness {}, engagement rate {}".format(
            m.get("hashtag_text"),
            m.get("count"),
            r.get("weight"),
            m.get("engagement_rate"))
        )
    # end for
# end analyse_hashtags


# Compute hashtag
def compute_hashtag(instagram_connector, hashtag_manager, hashtag_text, depth=5, min_count=3):
    """
    Compute hashtag
    :param instagram_connector:
    :param hashtag_manager:
    :param hashtag_text:
    :param depth:
    :param min_count:
    :return:
    """
    # Max id
    max_id = ''

    # Count
    count = 0
    
    # Pagination
    while True:
        # Log
        logging.getLogger(pystr.LOGGER).info(u"Going through page {} for hashtag {}".format(count+1, hashtag_text))

        # Get hashtag feed
        hashtag_feed = instagram_connector.hashtag_feed(hashtag_text[1:], maxid=max_id)

        # For each items
        for item in hashtag_feed['items']:
            # If there is a caption
            if item['caption'] is not None:
                # Likes and comments
                like_count = item['like_count']
                try:
                    comment_count = item['comment_count']
                except KeyError:
                    comment_count = 0
                # end try

                # User info
                try:
                    user_info = instagram_connector.username_info(item['user']['pk'])['user']
                except TypeError:
                    continue
                # end try

                # Nb followers
                follower_count = user_info['follower_count']

                # Engagement rate
                try:
                    engagement_rate = (float(like_count) + float(comment_count)) / float(follower_count)
                except ZeroDivisionError:
                    continue
                # end try

                # Links computed
                computed_links = list()

                # For each combination of hashtags
                for hashtag1 in re.findall(r'\B(\#[a-zA-Z]+\b)(?!;)', item['caption']['text']):
                    # Log
                    logging.getLogger(pystr.LOGGER).info(u"Updating hashtag {}".format(hashtag1))

                    # Increment count
                    hashtag_manager.inc_hashtag(hashtag1)

                    # Increment engagement rate
                    hashtag_manager.inc_engagement_rate(hashtag1, engagement_rate)

                    # For other hashtags
                    for hashtag2 in re.findall(r'\B(\#[a-zA-Z]+\b)(?!;)', item['caption']['text']):
                        if hashtag1 != hashtag2 and (hashtag1, hashtag2) not in computed_links and (hashtag2, hashtag1) not in computed_links:
                            # Add other hashtag
                            hashtag_manager.add(hashtag2)

                            # Inc link between hashtags
                            hashtag_manager.inc_link(hashtag1, hashtag2)

                            # Link computed
                            computed_links.append((hashtag1, hashtag2))
                        # end if
                    # end for
                # end for
            # end if
        # end for

        # Inc count
        count += 1

        # Next max id
        if 'next_max_id'in hashtag_feed.keys() and count < depth:
            max_id = hashtag_feed['next_max_id']
        else:
            break
        # end if
    # end while

    # Remove useless hashtags
    hashtag_manager.delete_by_count(min_count=depth * min_count)
# end compute_hashtag


# Hashtag analysis
def hashtag_analysis(instagram_connector, config, hashtag_to_updade="", depth=5, min_count=3):
    """
    Hashtag analysis
    :param instagram_connector:
    :param config:
    :return:
    """
    # Next max id
    next_max_id = ''

    # Computed hashtags
    computed_hashtags = list()

    # Hashtag manager
    hashtag_manager = hashtags.HashtagManager()

    # Hashtag specifies
    if hashtag_to_updade != "":
        compute_hashtag(instagram_connector, hashtag_manager, "#" + hashtag_to_updade, depth=depth, min_count=min_count)
        return
    # end if

    # Pagination
    while True:
        # Get user feed
        user_feed = instagram_connector.user_feed(max_id=next_max_id)

        # For each feed item
        for item in user_feed['items']:
            # For each hashtags
            for hashtag in re.findall(r'\B(\#[a-zA-Z]+\b)(?!;)', item['caption']['text']):
                # Add or get
                hashtag_manager.add(hashtag)

                # Not yet computed
                if hashtag not in computed_hashtags:
                    compute_hashtag(instagram_connector, hashtag_manager, hashtag, depth=depth, min_count=min_count)
                # end if
            # end for
        # end for

        # Next max id
        if 'next_max_id' in user_feed.keys():
            next_max_id = user_feed['next_max_id']
        else:
            break
        # end if
    # end for
# end hashtag_analysis


# Export hashtag database to GraphML
def export_graphML(file_path):
    """
    Export hashtag database to GraphML
    :param file_path:
    :return:
    """
    # Hashtag manager
    hashtag_manager = hashtags.HashtagManager()

    # Open output file
    f_out = codecs.open(file_path, 'w', encoding='utf-8')

    # Write
    hashtag_manager.export_graphML(f_out)
# end export_graphML
