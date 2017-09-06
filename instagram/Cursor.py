#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Imports
import time
import json


# Base class for cursor
class Cursor(object):
    """
    Base class for cursor
    """

    # Constructor
    def __init__(self, descriptor, page_size=20):
        """
        Constructor
        :param user_id: User's ID
        :param page_size:
        """
        # Properties
        self._descriptor = descriptor
        self._page_size = page_size
        self._items = []
        self._end_cursor = None

        # Loads
        self._load_items()
    # end __init__

    ##################################################
    # Override
    ##################################################

    # Iter
    def __iter__(self):
        """
        Iter
        :return:
        """
        return self
    # end __iter__

    # Next
    def next(self):
        """
        Next
        :return:
        """
        if len(self._items) == 0:
            n_items = self._load_items()
            if n_items == 0:
                raise StopIteration()
            # end if
        # end if

        return self._items.pop()
    # end next

    ##################################################
    # Private
    ##################################################

    # Load items
    def _load_items(self):
        """
        Load followers
        :return:
        """
        if self._descriptor.connector.logged():
            # Get items URL
            if self._end_cursor is None:
                items_url = self._descriptor.url_items.format(self._descriptor.connector.user_id(), 20)
            else:
                items_url = self._descriptor.url_items_next.format(self._descriptor.connector.user_id(), 20,
                                                                   self._end_cursor)
            # end if

            # POST request
            req = self._descriptor.connector.request()
            req.headers.update({'referer': self._descriptor.referer.format(self._descriptor.connector.username())})
            print(req.headers)
            items_response = req.get(items_url)
            print(items_response)

            # 200 Ok
            if items_response.status_code == 200:
                # Wait 10 seconds
                time.sleep(10)

                # Parse to JSON
                json_data = json.loads(items_response.text)
                print(json_data)
                # Next page cursor
                self._end_cursor = json_data['data']['user'][self._descriptor.edge_type]['page_info'][
                    'end_cursor']

                # Add users
                for node in json_data['data']['user'][self._descriptor.edge_type]['edges']:
                    self._items.append(node['node'])
                # end for
                return len(self._items)
            # end if
        # end if

        return 0
    # end _load_items

# end Cursor
