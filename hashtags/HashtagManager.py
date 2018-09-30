#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : twitter.TweetBotConnector.py
# Description : Main class to connect with Twitter API.
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

import datetime
from pyInstaBot.patterns.singleton import singleton
import pyInstaBot.db.obj
from sqlalchemy import and_, not_
import logging
from datetime import timedelta
import pyInstaBot.tools.strings as pystr
import pyInstaBot.db.obj
import pyInstaBot.instagram
import time
from neo4jrestclient.client import GraphDatabase, Relationship, Node
import numpy as np
import re


# Manage hashtags from the DB
@singleton
class HashtagManager(object):
    """
    Manage hashtags from the DB
    """

    # Constructor
    def __init__(self, config):
        """
        Constructor
        :param database_connector:
        """
        # DB session
        self._neo4j = pyInstaBot.db.Neo4jConnector()

        # Config
        self._config = config

        # Logger
        self._logger = logging.getLogger(name=pystr.LOGGER)
    # end __init__

    # Get hashtags
    def get_hashtags(self):
        """
        Get hashtags
        :return:
        """
        return self._neo4j.get_hashtags()
    # end get_hashtags

    # Get links
    def get_links(self):
        """
        Get links
        :return:
        """
        return self._neo4j.get_links()
    # end get_links

    # Add hashtag
    def add(self, hashtag_text):
        """
        Add hashtags
        :param hashtag_text:
        :return:
        """
        return self._neo4j.add_hashtag(hashtag_text=hashtag_text)
    # end add

    # Increment hashtag count
    def inc_hashtag(self, hashtag_text):
        """
        Increment hashtag count
        :param hashtag:
        :return:
        """
        # Increment
        self._neo4j.inc_hashtag(hashtag_text=hashtag_text)
    # end inc_hashtag

    # Increment engagement rate
    def inc_engagement_rate(self, hashtag_text, engagement_rate):
        """
        Increment engagement rate
        :param hashtag_text:
        :param engagement_rate:
        :return:
        """
        # Inc
        self._neo4j.inc_engagement_rate(hashtag_text, engagement_rate)
    # end inc_engagement_rate

    # Increment link
    def inc_link(self, hashtag1_text, hashtag2_text):
        """
        Increment link
        :param hashtag1_text:
        :param hastag2_text:
        :return:
        """
        # Inc
        self._neo4j.inc_link(hashtag1_text, hashtag2_text)
    # end inc_link

    # Delete node with less than a certain amount of count
    def delete_by_count(self, min_count):
        """
        Delete node
        :param min_count:
        :return:
        """
        self._neo4j.delete_by_count(min_count)
    # end delete_by_count

    # Parse hashtags in text
    def parse_hashtags(self, text, remove_hash=True):
        """
        Parse hashtags in text
        :param text:
        :return:
        """
        hashtag_list = list()
        # For each combination of hashtags
        for h in re.findall(r'\B(\#[a-zA-Zéüèàä0-9]+\b)(?!;)', text):
            if remove_hash:
                hashtag_list.append(h[1:])
            else:
                hashtag_list.append(h)
            # end if
        # end for
        return hashtag_list
    # end parse_hashtag

    # Get linked hashtags
    def related_hashtags(self, hashtags):
        """
        Get linked hashtags
        :param hashtags:
        :return:
        """
        # Query
        query = """MATCH p=(n:Hashtag)-[r:LINKED]->(m:Hashtag)
        WHERE n.hashtag_text in """

        # Create array of nodes
        query += "["
        for hashtag in hashtags:
            query += "\"#{}\"".format(hashtag)
        # end for
        query += "]"

        # End
        query += """ and m.count > 30
        RETURN DISTINCT m
        ORDER BY m.engagement_rate DESC"""

        # Execute
        return self._neo4j.execute(query, (Node))
    # end related_hashtags

    # Get hashtags of interest
    def interest_hashtags(self, hashtags):
        """
        Get hashtags of interest
        :param hashtags:
        :return:
        """
        # Create array of nodes
        nodes_query = u"["
        for hashtag in hashtags:
            nodes_query += u"\"#{}\",".format(hashtag)
        # end for
        nodes_query = nodes_query[:-1]
        nodes_query += u"]"

        query = u"""MATCH p=(n:Hashtag)-[r:LINKED]->(m:Hashtag)
                        WHERE n.hashtag_text IN """

        # Source
        query += nodes_query

        # Dest
        query += u""" AND NOT m.hashtag_text IN """
        query += nodes_query

        # End
        query += u""" AND m.count > 30
                RETURN n, r, m
                ORDER BY (2.0 * r.weight * m.engagement_rate) / (r.weight + m.engagement_rate) DESC"""

        # Execute
        return self._neo4j.execute(query, (Node, Relationship, Node))
    # end related_hashtags

    # Advisable hashtags of interest
    def advisable_hashtags(self, hashtags):
        """
        Advisable hashtags of interest
        :param hashtags:
        :return:
        """
        # Number of hashtags to generate
        n_hashtag_to_generate = 17 - len(hashtags)

        # Empty if no hashtags
        if n_hashtag_to_generate <= 0:
            return u""
        # end if

        # Get interest hashtags
        interest_hashtags = self.interest_hashtags(hashtags)

        # List of hashtags
        hashtag_list = list()
        hashtag_scores = dict()
        for (n, r, m) in interest_hashtags:
            if m.get('hashtag_text') not in hashtag_scores:
                hashtag_scores[m.get('hashtag_text')] = (r.get('weight'), m.get('engagement_rate'))
            else:
                link_weight = hashtag_scores[m.get('hashtag_text')][0]
                hashtag_scores[m.get('hashtag_text')] = (link_weight + r.get('weight'), m.get('engagement_rate'))
            # end if
        # end for

        # Compute F-score
        for hashtag_text in hashtag_scores.keys():
            # Info
            link_weight, engagement_rate = hashtag_scores[hashtag_text]

            # Compute f1
            hashtag_scores[hashtag_text] = (2.0 * link_weight * engagement_rate) + (link_weight + engagement_rate)

            # Filter
            ok = True
            for word in self._config.forbidden_words:
                if word in hashtag_text:
                    ok = False
                # end if
            # end for

            # Add
            if ok:
                hashtag_list.append((hashtag_text, hashtag_scores[hashtag_text]))
            # end if
        # end for

        # Sort
        hashtag_list.sort(key=lambda tup: tup[1], reverse=True)
        hashtag_list = [el[0] for el in hashtag_list]

        # Select a random sample
        selected_hashtags = list()
        n_generated_hashtags = 0
        for h in hashtag_list:
            if np.random.rand() < 0.5:
                selected_hashtags.append(h)
                n_generated_hashtags += 1
            # end if

            # Limit
            if n_generated_hashtags == n_hashtag_to_generate:
                break
            # end if
        # end for

        # Join
        hashtag_string = u""
        for h in selected_hashtags:
            hashtag_string += h
            hashtag_string += u" "
        # end for

        return hashtag_string
    # end advisable_hashtags

    # Export to GraphML
    def export_graphML(self, f_out):
        """
        Export to GraphML
        :param file_path:
        :return:
        """
        # Write header
        f_out.write(u'<?xml version="1.0" encoding="UTF-8"?><graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd"><graph id="pyInstaBot" edgedefault="undirected">')

        # Write keys
        f_out.write(u'<key id="engagement_rate" for="node" attr.name="engagement_rate" attr.type="double"/>')
        f_out.write(u'<key id="count" for="edge" attr.name="count" attr.type="integer"/>')

        # Write each node
        for hashtag in self.get_hashtags():
            # Engagement rate
            try:
                engagement_rate = hashtag[0].get('engagement_rate') / hashtag[0].get('count')
            except ZeroDivisionError:
                engagement_rate = 0.0
            # end try

            # Write
            f_out.write(
                u'<node id="{}"><data key="engagement_rate">{}</data></node>'.format(
                    hashtag[0].get('hashtag_text'),
                    engagement_rate
                )
            )
        # end for

        #  Write each links
        for index, (node1, edge, node2) in enumerate(self.get_links()):
            # Edge's weight
            weight = (2.0 * edge.get('count')) / (node1.get('count') + node2.get('count'))

            # Write node
            f_out.write(
                u'<edge id="{}" source="{}" target="{}"><data key="weight">{}</data></edge>'.format(
                    index,
                    node1.get('hashtag_text'),
                    node2.get('hashtag_text'),
                    weight
                )
            )
        # end for

        # Write footer
        f_out.write(u"</graph></graphml>")
    # end export_graphML

# end HashtagManager
