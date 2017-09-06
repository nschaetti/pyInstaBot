#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Imports


# Edge descriptor
class EdgeDescription(object):
    """
    Edge descriptor
    """

    # Informations
    edge_type = ''
    referer = ''
    url_items = 'https://www.instagram.com/graphql/query/?query_id=17851374694183129&variables=%7B"id"%3A"{}"%2C"first"%3A{}%7D'
    url_items_next = 'https://www.instagram.com/graphql/query/?query_id=17851374694183129&variables=%7B"id"%3A"{}"%2C"first"%3A{}%2C"after"%3A"{}"%7D'

    # Constructor
    def __init__(self, connector, edge_type, referer):
        """
        Constructor
        :param edge_type:
        :param referer:
        :param url_items:
        :param url_items_next:
        """
        # Properties
        self.connector = connector
        self.edge_type = edge_type
        self.referer = referer
    # end __init__

    #############################################
    # Override
    #############################################

    # Transform to object
    def __call__(self, *args, **kwargs):
        """
        Transform to object
        :param args:
        :param kwargs:
        :return:
        """
        pass
    # end __call__

# end EdgeDescriptor
