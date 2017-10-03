#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Imports
import logging
import time
import datetime
import json
from db.obj.User import User


# Followers cursor
class FollowersCursor(object):
    """
    Followers cursor
    """

    # URLs
    _edge = 'edge_followed_by'
    _referer = 'https://www.instagram.com/{}/followers/'
    _url_followers = 'https://www.instagram.com/graphql/query/?query_id=17851374694183129&variables=%7B"id"%3A"{}"%2C"first"%3A{}%7D'
    _url_followers_next = 'https://www.instagram.com/graphql/query/?query_id=17851374694183129&variables=%7B"id"%3A"{}"%2C"first"%3A{}%2C"after"%3A"{}"%7D'
    _id = 17845312237175864

    # Constructor
    def __init__(self, connector, page_size=20):
        """
        Constructor
        :param user_id: User's ID
        :param page_size:
        """
        # Properties
        self._connector = connector
        self._page_size = page_size
        self._users = []
        self._end_cursor = None

        # Loads
        self._load_followers()
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
        if len(self._users) == 0:
            n_users = self._load_followers()
            if n_users == 0:
                raise StopIteration()
            # end if
        # end if

        return self._users.pop()
    # end next

    ##################################################
    # Private
    ##################################################

    # Load followers
    def _load_followers(self):
        """
        Load followers
        :return:
        """
        if self._connector.logged():
            # Get folowers URL
            if self._end_cursor is None:
                followers_url = self._url_followers.format(self._connector.user_id(), 20)
            else:
                followers_url = self._url_followers_next.format(self._connector.user_id(), 20, self._end_cursor)
            # end if

            # POST request
            req = self._connector.request()
            req.headers.update({'referer': self._referer.format(self._connector.username())})
            print(self._referer.format(self._connector.username()))
            followers_response = req.post(followers_url)
            print(followers_response.text)

            # 200 Ok
            if followers_response.status_code == 200:
                # Wait 10 seconds
                time.sleep(10)

                # Parse to JSON
                json_data = json.loads(followers_response.text)
                print(json_data['data']['user'].keys())
                # Next page cursor
                self._end_cursor = json_data['data']['user'][self._edge]['page_info']['end_cursor']

                # Add users
                for node in json_data['data']['user'][self._edge]['edges']:
                    user = node['node']
                    self._users.append(User(user_id=user['id'], user_username=user['username'],
                                            user_full_name=user['full_name'],
                                            user_profile_pic_url=user['profile_pic_url'],
                                            user_is_verified=user['is_verified'],
                                            user_followed_by_viewer=user['followed_by_viewer'],
                                            user_requested_by_viewer=user['requested_by_viewer']))
                # end for
                return len(self._users)
            # end if
        # end if

        return 0
    # end _load_followers

# end FollowersCursor
