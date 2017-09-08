#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


# A hashtag
class Hashtag(object):

    # Properties
    name = "",
    id = 0,
    media_count = 0

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
        return u"(name={}, id={}, media_count={})".format(self.name, self.id, self.media_count)
    # end __unicode__

    def __str__(self):
        """
        To unicode
        :return:
        """
        return "(name={}, id={}, media_count={})".format(self.name, self.id, self.media_count)
    # end __unicode__

# end Media
