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
from obj.Hashtag import Hashtag
from obj.Media import Media
from obj.User import User
from obj.Place import Place


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

        # User timeline
        self.home_timeline = EdgeDescription(
                connector=self,
                root='graphql',
                data_type='user',
                edge_type='edge_web_feed_timeline',
                obj_class=Media,
                query_id="",
                variables={},
                url='https://www.instagram.com/?__a=1'
            )

        # User timeline
        self.user_timeline = EdgeDescription(
                connector=self,
                root='data',
                data_type='user',
                edge_type='edge_owner_to_timeline_media',
                obj_class=Media,
                query_id="17888483320059182",
                variables={'id': user_id},
                url='https://www.instagram.com/graphql/query/'
            )

        # Followers
        self.followers = EdgeDescription(
                connector=self,
                root='data',
                data_type='user',
                edge_type='edge_followed_by',
                obj_class=User,
                query_id="17851374694183129",
                variables={'id': user_id},
                url='https://www.instagram.com/graphql/query/'
            )

        # Following
        self.following = EdgeDescription(
                connector=self,
                root='data',
                data_type='user',
                edge_type='edge_follow',
                obj_class=User,
                query_id="17874545323001329",
                variables={'id': user_id},
                url="https://www.instagram.com/graphql/query/"
            )

        # Following
        self.following = EdgeDescription(
                connector=self,
                root='data',
                data_type='user',
                edge_type='edge_web_discover_media',
                obj_class=User,
                query_id="17863787143139595",
                variables={'id': user_id},
                url="https://www.instagram.com/graphql/query/"
            )
    # end __init__

    ########################################################
    # Public
    ########################################################

    # Search
    def search(self, keyword):
        """
        Search
        :param keyword:
        :return:
        """
        # Result
        users = list()
        places = list()
        hashtags = list()

        # Logged ?
        if self._logged:
            # URL
            url = "https://www.instagram.com/web/search/topsearch/?context=blended&query={}".format(keyword)

            # GET request
            req = self._req
            req.headers.update({'authority': u"www.instagram.com"})
            req.headers.update({'method': u"GET"})
            req.headers.update({'path': url.replace(u"https://www.instagram.com", u"")})
            req.headers.update({'scheme': 'https'})
            req.headers.update(
                {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'})
            req.headers.update({'accept-encoding': 'gzip, deflate, br'})
            req.headers.update({'accept-language': 'en-US,en;q=0.8,et;q=0.6,fr;q=0.4'})
            req.headers.update({'cache-control': 'no-cache'})
            req.headers.update({
                                   'cookie': u"mid=WRMdNAAEAAFPvuqh4JN4sLHQtwc3; fbm_124024574287414=base_domain=.instagram.com; ig_oia_dismiss=true; sessionid=IGSCf307fdc0fb36298a90efc94694b2de43158b500080592a4b2197ae6ce7096caa%3ACZWly9z3Xubg4Or9vzVwO9FOoQVwwDOm%3A%7B%22_auth_user_id%22%3A2926312088%2C%22_auth_user_backend%22%3A%22accounts.backends.CaseInsensitiveModelBackend%22%2C%22_auth_user_hash%22%3A%22%22%2C%22_token_ver%22%3A2%2C%22_token%22%3A%222926312088%3AH2LpNGEpJ3FfMeB6a4WHk6VWXsiCrdCD%3Afee4341ce963c84af3b75d02e0ab1fa645ba7cd2fab4cc3bef8ae9333eee433e%22%2C%22_platform%22%3A4%2C%22last_refreshed%22%3A1504734160.2970302105%2C%22asns%22%3A%7B%22time%22%3A1504734221%2C%222.37.52.220%22%3A30722%7D%7D; ig_vw=412; ig_pr=2.625; ig_vh=660; fbsr_124024574287414=2VSpYn7Khc60NFfDLIfkFYGNiO4pjrg-c6BtJ4Ln49M.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUNLZF9lN21fby1qQWxzaldmWExzaDJPRTN5OUJHTlpxYmQwS3A2WHVxcjNwYXIycERvUEMyMTNOUHN4T0FRNXowdHhqdVU5QzRSZE9jQWsyX3RmRXk2NlAtd3V5dkhJVjVYcERtY29CS1B1OEpXSUY3cGJsYkVXTHhrZGdPTnBJZFNleXloNDZWQ2dmS3o1Y3JxRk9KaGIyS0JJMWRCRjh2OXJGN1hpeEU4a2hGVHRLMEZ6eXB3VXhzZWNHS1RsRjNyOGV1ZEF1NnRmSWhIV3pqM1ZsUnIybXRrdTg2UndvajNvU3dFRUI4NmRvZVBWV3lSOGkzaUdVU01rQm93Q3pBUWlwd3ZWQTd6WG1lRThRa3VHaWMyWG1FLXUybVdsTzdMQjJEZ2wwVVpncms5dndXNEVUSzBWZWtXblZIRjRhTEhtdG5CVEoxMzd6UXdLRGdzUld6MiIsImlzc3VlZF9hdCI6MTUwNDgwNDc5NCwidXNlcl9pZCI6IjEwMTY4ODU4NzIifQ; csrftoken=nf8biutIZLEsN45mB31aYrLb5QmWvOq6; rur=ASH; ds_user_id=2926312088"})
            req.headers.update({'pragma': 'no-cache'})
            req.headers.update({'upgrade-insecure-requests': '1'})
            req.headers.update({
                                   'user-agent': u"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"})
            items_response = req.get(url)

            # 200 Ok
            if items_response.status_code == 200:
                # Wait 2 seconds
                time.sleep(2)

                # Parse to JSON
                json_data = json.loads(items_response.text)

                # For each users
                for user in json_data['users']:
                    user_obj = self._dict_to_obj(user['user'], User())
                    users.insert(0, user_obj)
                # end for

                # For each places
                for place in json_data['places']:
                    place_obj = self._dict_to_obj(place['place'], Place())
                    places.insert(0, place_obj)
                # end for

                # For each hashtags
                for hashtag in json_data['hashtags']:
                    hashtag_obj = self._dict_to_obj(hashtag['hashtag'], Hashtag())
                    hashtags.insert(0, hashtag_obj)
                # end for
            # end if
        # end if

        return users, places, hashtags
    # end search

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

    ################################################
    # Private
    ################################################

    # Dict to object
    def _dict_to_obj(self, d, obj):
        """
        Dict to object
        :param d:
        :param obj:
        :return:
        """
        for key in d.keys():
            setattr(obj, key, d[key])
        # end for
        return obj
    # end _dict_to_obj

# end Instagram
