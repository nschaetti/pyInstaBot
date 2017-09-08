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
            # Connector
            desc = self._descriptor

            # Get items URL
            items_url = desc.get_url(end_cursor=self._end_cursor, count=20)

            # GET request
            req = self._descriptor.connector.request()
            req.headers.update({'authority': u"www.instagram.com"})
            req.headers.update({'method': u"GET"})
            req.headers.update({'path': items_url.replace(u"https://www.instagram.com", u"")})
            req.headers.update({'scheme': 'https'})
            req.headers.update({'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'})
            req.headers.update({'accept-encoding': 'gzip, deflate, br'})
            req.headers.update({'accept-language': 'en-US,en;q=0.8,et;q=0.6,fr;q=0.4'})
            req.headers.update({'cache-control': 'no-cache'})
            req.headers.update({'cookie': u"mid=WRMdNAAEAAFPvuqh4JN4sLHQtwc3; fbm_124024574287414=base_domain=.instagram.com; ig_oia_dismiss=true; sessionid=IGSCf307fdc0fb36298a90efc94694b2de43158b500080592a4b2197ae6ce7096caa%3ACZWly9z3Xubg4Or9vzVwO9FOoQVwwDOm%3A%7B%22_auth_user_id%22%3A2926312088%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_token_ver%22%3A2%2C%22_token%22%3A%222926312088%3AH2LpNGEpJ3FfMeB6a4WHk6VWXsiCrdCD%3Afee4341ce963c84af3b75d02e0ab1fa645ba7cd2fab4cc3bef8ae9333eee433e%22%2C%22_platform%22%3A4%2C%22last_refreshed%22%3A1504734160.2970302105%2C%22asns%22%3A%7B%22time%22%3A1504734221%2C%222.37.52.220%22%3A30722%7D%7D; ig_vw=412; ig_pr=2.625; ig_vh=660; fbsr_124024574287414=2VSpYn7Khc60NFfDLIfkFYGNiO4pjrg-c6BtJ4Ln49M.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUNLZF9lN21fby1qQWxzaldmWExzaDJPRTN5OUJHTlpxYmQwS3A2WHVxcjNwYXIycERvUEMyMTNOUHN4T0FRNXowdHhqdVU5QzRSZE9jQWsyX3RmRXk2NlAtd3V5dkhJVjVYcERtY29CS1B1OEpXSUY3cGJsYkVXTHhrZGdPTnBJZFNleXloNDZWQ2dmS3o1Y3JxRk9KaGIyS0JJMWRCRjh2OXJGN1hpeEU4a2hGVHRLMEZ6eXB3VXhzZWNHS1RsRjNyOGV1ZEF1NnRmSWhIV3pqM1ZsUnIybXRrdTg2UndvajNvU3dFRUI4NmRvZVBWV3lSOGkzaUdVU01rQm93Q3pBUWlwd3ZWQTd6WG1lRThRa3VHaWMyWG1FLXUybVdsTzdMQjJEZ2wwVVpncms5dndXNEVUSzBWZWtXblZIRjRhTEhtdG5CVEoxMzd6UXdLRGdzUld6MiIsImlzc3VlZF9hdCI6MTUwNDgwNDc5NCwidXNlcl9pZCI6IjEwMTY4ODU4NzIifQ; csrftoken=nf8biutIZLEsN45mB31aYrLb5QmWvOq6; rur=ASH; ds_user_id=2926312088"})
            req.headers.update({'pragma': 'no-cache'})
            req.headers.update({'upgrade-insecure-requests': '1'})
            req.headers.update({'user-agent': u"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"})
            items_response = req.get(items_url)

            # 200 Ok
            if items_response.status_code == 200:
                # Wait 2 seconds
                time.sleep(2)

                # Parse to JSON
                json_data = json.loads(items_response.text)

                # Next page cursor
                self._end_cursor = desc.get_end_cursor(json_data)

                # Add users
                for node in desc.get_items(json_data):
                    self._items.insert(0, self._descriptor(node))
                # end for
                return len(self._items)
            # end if
        # end if

        return 0
    # end _load_items

# end Cursor
