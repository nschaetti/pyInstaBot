#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Imports
import logging
import requests
import time
import random
import json


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
    _user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")

    # Accepted language
    _accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'

    # Constructor
    def __init__(self, username, password, debug=False):
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
                like = self.s.post(url_likes)
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
        if (self.login_status):
            url_unlike = self.url_unlike % (media_id)
            try:
                unlike = self.s.post(url_unlike)
            except:
                self.write_log("Except on unlike!")
                unlike = 0
            # end
            return unlike
        # end if
    # end unlike

    # Post a comment
    def comment(self, media_id, comment_text):
        """
        Send http request to comment
        """
        if self._logged:
            comment_post = {'comment_text' : comment_text}
            url_comment = self.url_comment % media_id
            try:
                comment = self.s.post(url_comment, data=comment_post)
                if comment.status_code == 200:
                    self.comments_counter += 1
                    log_string = 'Write: "%s". #%i.' % (comment_text, self.comments_counter)
                    self.write_log(log_string)
                return comment
            except:
                self.write_log("Except on comment!")
        return False
    # end comment

    # Follow
    def follow(self, user_id):
        """
        Send http request to follow
        """
        if self._logged:
            url_follow = self.url_follow % (user_id)
            try:
                follow = self.s.post(url_follow)
                if follow.status_code == 200:
                    self.follow_counter += 1
                    log_string = "Followed: %s #%i." % (user_id, self.follow_counter)
                    self.write_log(log_string)
                return follow
            except:
                self.write_log("Except on follow!")
        return False

    def unfollow(self, user_id):
        """ Send http request to unfollow """
        if (self.login_status):
            url_unfollow = self.url_unfollow % (user_id)
            try:
                unfollow = self.s.post(url_unfollow)
                if unfollow.status_code == 200:
                    self.unfollow_counter += 1
                    log_string = "Unfollow: %s #%i." % (user_id, self.unfollow_counter)
                    self.write_log(log_string)
                return unfollow
            except:
                self.write_log("Exept on unfollow!")
        return False

# end Instagram
