#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : twitter.TweetBotConnector.py
# Description : Main class to connect with Twitter API.
# Date : 21.05.2018 14:43:00
#
# This file is part of the Tanaturf.
# The Tanaturf is a set of free software:
# you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tanaturf is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Tanaturf.  If not, see <http://www.gnu.org/licenses/>.
#

# Imports
import neo4jrestclient.exceptions
from neo4jrestclient.client import GraphDatabase, Relationship, Node
from pyInstaBot.patterns.singleton import singleton


# Neo4j connector
@singleton
class Neo4jConnector(object):
    """
    Neo4j connector
    """

    # Constructor
    def __init__(self, user, password, uri="http://localhost:7474"):
        """
        Constructor
        :param uri:
        :param user:
        :param password:
        """
        # DB
        self.db = GraphDatabase(uri, username=user, password=password)

        # Create labels
        self.hashtag_nodes = self.db.labels.create("Hashtag")

        # List
        self.hashtags = list()
    # end __init__

    #################################
    # PROPERTIES
    #################################

    # Number of hashtags
    @property
    def n_hashtags(self):
        """
        Number of hashtags
        :return:
        """
        return len(self.hashtags)
    # end n_hashtags

    #################################
    # PUBLIC
    #################################

    # Delete by count
    def delete_by_count(self, min_count):
        """
        Delete by count
        :param min_count:
        :return:
        """
        # Remove nodes
        self._execute_query(
            "MATCH (m:Hashtag) WHERE m.count < {} DETACH DELETE m".format(min_count)
        )
    # end delete_by_count

    # Increment hashtag count
    def inc_hashtag(self, hashtag_text):
        """
        Increment hashtag count
        :param hashtag_text:
        :return:
        """
        # Get hashtag node
        hashtag_node = self.get_hashtag(hashtag_text=hashtag_text)

        # Create if does not exists
        if hashtag_node is None:
            hashtag_node = self.add_hashtag(hashtag_text=hashtag_text)
        # end if

        # Increment
        hashtag_node.set("count", hashtag_node.get("count") + 1)
    # end inc_hashtag

    # Increment engagement rate
    def inc_engagement_rate(self, hashtag_text, engagement_rate):
        """
        Increment engagement rate
        :param hashtag_text:
        :param engagement_rate:
        :return:
        """
        # Get hashtag node
        hashtag_node = self.get_hashtag(hashtag_text=hashtag_text)

        # Create if does not exists
        if hashtag_node is None:
            hashtag_node = self.add_hashtag(hashtag_text=hashtag_text)
        # end if

        # Inc
        hashtag_node.set("engagement_rate_sum", hashtag_node.get("engagement_rate_sum") + engagement_rate)
        hashtag_node.set("engagement_rate", hashtag_node.get("engagement_rate_sum") / float(hashtag_node.get("count")))
    # end inc_engagement_rate

    #  Increment link
    def inc_link(self, hashtag1_text, hashtag2_text):
        """
        Increment link between two hashtags
        :param hashtag1_text:
        :param hashtag2_text:
        :return:
        """
        # Get both hashtag
        hashtag1 = self.get_hashtag(hashtag1_text)
        hashtag2 = self.get_hashtag(hashtag2_text)

        # Get already existing relationship
        rel = self.get_link(hashtag1, hashtag2)

        # Create if does not exist
        if rel is None:
            rel = self.link(hashtag1_text, hashtag2_text)
        # end if

        # Inc
        rel.set("count", rel.get("count") + 1)
        rel.set("weight", 2.0 * rel.get("count") / float(hashtag1.get("count") + hashtag2.get("count")))
    # end inc_link

    # Add hashtag node
    def add_hashtag(self, hashtag_text):
        """
        Add a hashtag node
        :param hashtag_text:
        :return:
        """
        # Get hashtag node
        hashtag_node = self.get_hashtag(hashtag_text=hashtag_text)

        # Create if does not exists
        if hashtag_node is None:
            # Create hashtag
            hashtag_node = self.db.nodes.create(
                hashtag_text=hashtag_text,
                Label=hashtag_text,
                linked_in=0,
                linked_out=0,
                count=0,
                engagement_rate_sum=0.0,
                engagement_rate=0.0
            )

            # Add to list and DB
            self.hashtag_nodes.add(hashtag_node)
            self.hashtags.append(hashtag_node)
        # end if

        return hashtag_node
    # end add_user_node

    # Get hashtag
    def get_hashtag(self, hashtag_text):
        """
        Get a hashtag
        :param hashtag:
        :return:
        """
        # Query
        results = self.hashtag_nodes.get(hashtag_text=hashtag_text)

        # Found
        if len(results) == 0:
            return None
        else:
            return results[0]
        # end if
    # end get_hashtag

    # Get hashtags
    def get_hashtags(self):
        """
        Get hashtags
        :return:
        """
        # Query
        q = u"MATCH (m:Hashtag) RETURN m"

        # Get relationship
        result = self.db.query(
            q=q,
            returns=(Node)
        )

        # Check if found
        return result
    # end get_hashtags

    # Get links
    def get_links(self):
        """
        Get links
        :return:
        """
        # Query
        q = u"MATCH (m:Hashtag)-[r:LINKED]->(n:Hashtag) RETURN m, r, n"

        # Get relationship
        result = self.db.query(
            q=q,
            returns=(Node, Relationship, Node)
        )

        # Check if found
        return result
    # end get_links

    # Execute query
    def execute(self, query, returns):
        """
        Execute query
        :param query:
        :return:
        """
        return self.db.query(q=query, returns=returns)
    # end execute

    # Add a coocurrence relationship
    def link(self, hashtag1_text, hashtag2_text):
        """
        Add a quoted relationship
        :param user1:
        :param site:
        :return:
        """
        # Get both hashtag
        hashtag1 = self.get_hashtag(hashtag1_text)
        hashtag2 = self.get_hashtag(hashtag2_text)

        # Get already existing relationship
        rel = self.get_link(hashtag1, hashtag2)

        # Incremente out
        try:
            hashtag1.set("links", hashtag1.get("links") + 1)
        except neo4jrestclient.exceptions.NotFoundError:
            hashtag1.set("links", 1)
        # end try

        # Incremente in
        try:
            hashtag2.set("links", hashtag2.get("links") + 1)
        except neo4jrestclient.exceptions.NotFoundError:
            hashtag2.set("links", 1)
        # end try

        # Not exist
        if rel is None:
            rel = hashtag1.relationships.create("LINKED", hashtag2)
            rel.set("count", 1)
            rel.set("weight", 2.0 / float(hashtag1.get("count") + hashtag2.get("count")))
        else:
            rel.set("count", rel.get("count") + 1)
            rel.set("weight", 2.0 * rel.get("count") / float(hashtag1.get("count") + hashtag2.get("count")))
        # end if

        return rel
    # end linked_relationship

    # Get a LINKED relationship
    def get_link(self, hashtag1, hashtag2):
        """
        Get a linked relationship
        :param hashtag1:
        :param hashtag2:
        :return:
        """
        # Query
        q = u"MATCH (m:Hashtag)-[r:LINKED]->(n:Hashtag) WHERE m.hashtag_text=\"{}\" and n.hashtag_text=\"{}\" RETURN r".format(
            hashtag1.get('hashtag_text'), hashtag2.get('hashtag_text')
        )

        # Get relationship
        result = self.db.query(
            q=q,
            returns=(Relationship)
        )

        # Check if found
        if len(result) > 0:
            return result[0][0]
        else:
            return None
        # end if
    # end get_linked_relationship

    #################################
    # PRIVATE
    #################################

    # Execute query
    def _execute_query(self, q):
        """
        Execute query
        :param q:
        :return:
        """
        # Remove lone Twitter users
        return self.db.query(
            q=q
        )
    # end _execute_query

# end Neo4jConnector