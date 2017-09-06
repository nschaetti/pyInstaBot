#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Imports
import logging
import requests
import time
import random
import json
from FollowersCursor import FollowersCursor
from FollowingCursor import FollowingCursor
from EdgeDescriptor import EdgeDescription


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
    url_followers = 'https://www.instagram.com/graphql/query/?query_id=17851374694183129&variables=%7B"id"%3A"{}"%2C"first"%3A{}%7D'
    url_followers_next = 'https://www.instagram.com/graphql/query/?query_id=17851374694183129&variables=%7B"id"%3A"{}"%2C"first"%3A{}%2C"after"%3A"{}"%7D'

    # User agent
    _user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")

    # Accepted language
    _accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'

    # Constructor
    def __init__(self, user_id, username, password, debug=False):
        """
        Constructor
        :param username: Instagram username
        :param password: Instagram password
        :param debug: Debug mode?
        :return:
        """
        self._user_id = user_id
        self._username = username
        self._password = password
        self._debug = debug
        self._req = None
        self._csrftoken = None
        self._logged = False

        # Descriptor
        self.user_timeline = EdgeDescription(self, 'edge_owner_to_timeline_media',
                                             'https://www.instagram.com/n.schaetti.public/')
    # end __init__

    ########################################################
    # Public
    ########################################################

    # Logged?
    def logged(self):
        """
        Logged
        :return:
        """
        return self._logged
    # end logged

    # Get request
    def request(self):
        """
        Get request
        :return:
        """
        return self._req
    # end request

    # User's ID
    def user_id(self):
        """
        User's ID
        :return:
        """
        return self._user_id
    # end user_id

    # Username
    def username(self):
        """
        Username
        :return:
        """
        return self._username
    # end username

    # Login
    def login(self):
        """
        Login to Instagram
        :return:
        """
        logging.getLogger(u"pyInstaBot").info(u"Trying to login as {}".format(self._username))

        # Request
        self._req = requests.Session()

        # Update cookies
        self._req.cookies.update({'sessionid': '', 'mid': '', 'ig_pr': '1',
                               'ig_vw': '1920', 'csrftoken': '',
                               's_network': '', 'ds_user_id': ''})

        # Login post data
        login_post_data = {'username': self._username,
                           'password': self._password}

        # Update headers
        self._req.headers.update({'Accept-Encoding': 'gzip, deflate',
                               'Accept-Language': self._accept_language,
                               'Connection': 'keep-alive',
                               'Content-Length': '0',
                               'Host': 'www.instagram.com',
                               'Origin': 'https://www.instagram.com',
                               'Referer': 'https://www.instagram.com/',
                               'User-Agent': self._user_agent,
                               'X-Instagram-AJAX': '1',
                               'X-Requested-With': 'XMLHttpRequest'})

        # Get main page
        get_response = self._req.get(self.url)

        # Update header
        self._req.headers.update({'X-CSRFToken': get_response.cookies['csrftoken']})

        # Wait some time
        time.sleep(5 * random.random())

        # Get login response
        login_response = self._req.post(self.url_login, data=login_post_data, allow_redirects=True)

        # Check login
        if login_response.status_code == 200:
            # Login JSON
            login_json = json.loads(login_response.text)

            # Update headers
            self._req.headers.update({'X-CSRFToken': login_response.cookies['csrftoken']})

            # Update CSRF token
            self._csrftoken = login_response.cookies['csrftoken']

            # Wait
            time.sleep(5 * random.random())

            # Request main page
            r = self._req.get('https://www.instagram.com/')
            finder = r.text.find(self._username)

            # Try to find the username
            if finder != -1 and login_json['authenticated'] and login_json['user'] and login_json['status'] == u"ok":
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

    # Like a media
    def like(self, media_id):
        """
        Send http request to like media by ID
        """
        if self._logged:
            # Like URL
            url_likes = self.url_likes % media_id

            # Try send a POST
            try:
                like_response = self._req.post(url_likes)

                # 200 Ok
                if like_response.status_code == 200:
                    logging.getLogger(u"pyInstabot").info(u"Liking {}".format(media_id))
                # end if
            except:
                logging.getLogger(u"pyInstaBot").error(u"Error on like!")
            # end try
        # end if
    # end like

    # Unlike a media
    def unlike(self, media_id):
        """
        Send http request to unlike media by ID
        """
        if self._logged:
            # Unlike URL
            url_unlike = self.url_unlike % (media_id)

            try:
                # Request
                unlike_response = self._req.post(url_unlike)

                # 200 OK
                if unlike_response.status_code == 200:
                    logging.getLogger(u"pyInstaBot").info(u"Unliking {}".format(media_id))
                # end if
            except:
                logging.getLogger(u"Exception while unliking {}".format(media_id))
            # end try
        # end if
    # end unlike

    # Post a comment
    def comment(self, media_id, comment_text):
        """
        Send http request to comment a media
        """
        if self._logged:
            # POST data
            comment_post = {'comment_text': comment_text}

            # Comment URL
            url_comment = self.url_comment % media_id

            try:
                # POST request
                comment_response = self._req.post(url_comment, data=comment_post)

                # 200 response
                if comment_response.status_code == 200:
                    logging.getLogger(u"pyInstaBot").info(u"Writing \"{}\" to {}".format(comment_text, media_id))
                # end if
                return comment_response
            except:
                logging.getLogger(u"pyInstaBot").info(u"Error while posting a comment!")
            # end try
        # end if
        return False
    # end comment

    # Follow
    def follow(self, user_id):
        """
        Send http request to follow
        """
        if self._logged:
            # URL for follow
            url_follow = self.url_follow % (user_id)

            try:
                # POST request
                follow_response = self._req.post(url_follow)

                # 200 Ok
                if follow_response.status_code == 200:
                    logging.getLogger(u"pyInstaBot").info(u"Followeing {}".format(user_id))
                    return True
                # end if
            except:
                logging.getLogger(u"pyInstaBot").info(u"Exception while following {}!".format(user_id))
            # end try
        # end if
        return False
    # end follow

    # Unfollow
    def unfollow(self, user_id):
        """
        Send http request to unfollow
        """
        if self._logged:
            # Unfollow URL
            url_unfollow = self.url_unfollow % user_id

            try:
                # POST request
                unfollow_response = self._req.post(url_unfollow)

                # 200 Ok
                if unfollow_response.status_code == 200:
                    logging.getLogger(u"pyInstaBot").info(u"Unfollowing {}".format(user_id))
                    return True
                # end if
            except:
                logging.getLogger(u"pyInstaBot").info(u"Exception while unfollowing {}".format(user_id))
            # end try
        # end if
        return False
    # end unfollow

    # Get followers
    def followers(self):
        """
        Get the followers
        :param user_id:
        :return:
        """
        if self._logged:
            return FollowersCursor(self)
        # end if
    # end followers

    # Get following
    def following(self):
        """
        Get the following
        :param user_id:
        :return:
        """
        if self._logged:
            return FollowingCursor(self)
        # end if
    # end followers

# end Instagram
