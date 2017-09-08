#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


# An Instagram user
class User(object):

    # Properties
    id = 0,
    pk = "",
    username = '',
    full_name = '',
    is_private = False,
    profile_pic_url = '',
    is_verified = False,
    has_anonymous_profile_picture = False,
    follower_count = -1,
    byline = "",
    social_context = "",
    search_social_context = "",
    mutual_followers_count = -1,
    following = False,
    outgoing_request = False,
    unseen_count = -1,
    followed_by_viewer = False,
    requested_by_viewer = False

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        pass
    # end __init__

    ##############################################
    # Override
    ##############################################

    # To unicode
    def __unicode__(self):
        """
        To unicode
        :return:
        """
        return u"(id={}, username={}, full_name={}, profile_pic_url={}, is_verified={}, " \
               u"followed_by_viewer={}, requested_by_viewer={})"\
            .format(self.id, self.username, self.full_name, self.profile_pic_url, self.is_verified,
                    self.followed_by_viewer, self.requested_by_viewer)
    # end __unicode__

    def __str__(self):
        """
        To unicode
        :return:
        """
        return "(id={}, username={}, full_name={}, profile_pic_url={}, is_verified={}, " \
               "followed_by_viewer={}, requested_by_viewer={})" \
            .format(self.id, self.username.encode('ascii', 'ignore'),
                    self.full_name.encode('ascii', 'ignore'), self.profile_pic_url, self.is_verified,
                    self.followed_by_viewer, self.requested_by_viewer)
    # end __unicode__

# end Media
