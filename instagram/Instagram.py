#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Imports
import logging
import requests
import time
import random
import datetime


# Instagram connector
class Instagram(object):
    """
    Instagram connector
    """

    # URLs
    url = 'https://www.instagram.com/'
    url_tag = 'https://www.instagram.com/explore/tags/'
    url_likes = 'https://www.instagram.com/web/likes/%s/like/'
    url_unlike = 'https://www.instagram.com/web/likes/%s/unlike/'
    url_comment = 'https://www.instagram.com/web/comments/%s/add/'
    url_follow = 'https://www.instagram.com/web/friendships/%s/follow/'
    url_unfollow = 'https://www.instagram.com/web/friendships/%s/unfollow/'
    url_login = 'https://www.instagram.com/accounts/login/ajax/'
    url_logout = 'https://www.instagram.com/accounts/logout/'

    # User agent
    user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")

    # Accepted language
    accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'

    # Constructor
    def __int__(self, username, password, debug=False):
        """
        Constructor
        :param username: Instagram username
        :param password: Instagram password
        :param debug: Debug mode?
        :return:
        """
        self._username = username
        self._password = password
        self._debug = debug
        self._req = None
        self._csrftoken = None
        self._logged = False
    # end __init__

    # Login
    def login(self):
        """
        Login to Instagram
        :return:
        """
        logging.getLogger(u"pyInstaBot").info(u"Trying to login as {}".format(self._username))

        # Request
        req = requests.Session()

        # Update cookies
        req.cookies.update({'sessionid': '', 'mid': '', 'ig_pr': '1',
                               'ig_vw': '1920', 'csrftoken': '',
                               's_network': '', 'ds_user_id': ''})

        # Login post data
        login_post_data = {'username': self._username,
                           'password': self._password}

        # Update headers
        req.headers.update({'Accept-Encoding': 'gzip, deflate',
                               'Accept-Language': self.accept_language,
                               'Connection': 'keep-alive',
                               'Content-Length': '0',
                               'Host': 'www.instagram.com',
                               'Origin': 'https://www.instagram.com',
                               'Referer': 'https://www.instagram.com/',
                               'User-Agent': self.user_agent,
                               'X-Instagram-AJAX': '1',
                               'X-Requested-With': 'XMLHttpRequest'})

        # Get main page
        response = self.s.get(self.url)

        # Update header
        self._req.headers.update({'X-CSRFToken': response.cookies['csrftoken']})

        # Wait some time
        time.sleep(5 * random.random())

        # Get login response
        login = self._req.post(self.url_login, data=login_post_data, allow_redirects=True)

        # Update headers
        self._req.headers.update({'X-CSRFToken': login.cookies['csrftoken']})

        # Update CSRF token
        self._csrftoken = login.cookies['csrftoken']

        # Wait
        time.sleep(5 * random.random())

        # Check login
        if login.status_code == 200:
            # Request main page
            r = self.s.get('https://www.instagram.com/')
            finder = r.text.find(self._username)

            # Try to find the username
            if finder != -1:
                self._logged = True
                logging.getLogger(u"pyInstaBot").info(u"{} login success!".format(self._username))
            else:
                self._logged = False
                logging.getLogger(u"pyInstaBot").info(u"Login error! Check your login data!")
            # end if
        else:
            logging.getLogger(u"pyInstaBot").info(u"Login error! Connection error!")
        # end if
    # end login

    # Logged
    def logout(self):
        """
        Logged
        :return:
        """
        # Log
        logging.getLogger(u"pyInstaBot").info(u"Logging out...")

        try:
            # CSRF token
            logout_post = {'csrfmiddlewaretoken': self._csrftoken}

            # Call logout page
            self._req.post(self.url_logout, data=logout_post)

            # Log
            logging.getLogger(u"pyInstaBot").info(u"Logged out successfully!")

            # State
            self._logged = False
        except:
            # Error
            logging.getLogger(u"pyInstaBot").error(u"An error occurred while logging out!")
        # end try
    # end logout

# end Instagram
