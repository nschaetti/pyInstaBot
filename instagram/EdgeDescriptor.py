#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Imports
from obj.Media import Media


# Edge descriptor
class EdgeDescription(object):
    """
    Edge descriptor
    """

    # Informations
    #url_items = 'https://www.instagram.com/graphql/query/?query_id={}&variables=%7B"id"%3A"{}"%2C"first"%3A{}%7D'
    #url_items_next = 'https://www.instagram.com/graphql/query/?query_id={}&variables=%7B"id"%3A"{}"%2C"first"%3A{}%2C"after"%3A"{}"%7D'

    # Constructor
    def __init__(self, connector, root, data_type, edge_type, obj_class, query_id, variables, url):
        """
        Constructor
        :param edge_type:
        :param referer:
        :param url_items:
        :param url_items_next:
        """
        # Properties
        self.connector = connector
        self.root = root
        self.data_type = data_type
        self.edge_type = edge_type
        self.obj_class = obj_class
        self.query_id = query_id
        self.variables = variables
        self.url = url
    # end __init__

    #############################################
    # Public
    #############################################

    # Get URL
    def get_url(self, end_cursor=None, count=20):
        """
        Get URL
        :param next_cursor:
        :return:
        """
        # URL
        url = self.url

        # Add query_id
        if self.query_id != "":
            url += "?query_id=" + str(self.query_id)
        # end if

        # Add variables
        if len(self.variables.keys()) > 0:
            url += "&variables=%7B"
            for index, key in enumerate(self.variables.keys()):
                value = self.variables[key]
                if index != 0:
                    url += "%2C"
                # end if
                if type(value) is int:
                    url += '"{}"%3A"{}"'.format(key, value)
                else:
                    url += '"{}"%3A{}'.format(key, value)
                # end if
            # end for

            # First
            url += '%2C"first"%3A{}'.format(count)

            # Add cursor
            if end_cursor is not None:
                url += '%2C"after"%3A"{}"'.format(end_cursor)
            # end if

            # Close bracket
            url += "%7D"
        # end if

        return url
    # end get_url

    # Get items
    def get_items(self, json_data):
        """
        Get items
        :param json_data:
        :return:
        """
        return json_data[self.root][self.data_type][self.edge_type]['edges']
    # end get_items

    # Get end cursor
    def get_end_cursor(self, json_data):
        """
        Get end cursor
        :param json_data:
        :return:
        """
        return json_data[self.root][self.data_type][self.edge_type]['page_info']['end_cursor']
    # end get_end_cursor

    #############################################
    # Override
    #############################################

    # Transform to object
    def __call__(self, node):
        """
        Transform to object
        :param args:
        :param kwargs:
        :return:
        """
        # Create the object
        obj = self.obj_class()

        # For each key
        for key in node['node'].keys():
            if key[:2] == '__':
                key_attr = key[2:]
            else:
                key_attr = key
            # end if
            setattr(obj, key_attr, node['node'][key])
        # end for

        return obj
    # end __call__

# end EdgeDescriptor
