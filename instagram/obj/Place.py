#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


# A place
class Place(object):

    # Properties
    location = {},
    title = "",
    subtitle = u"",
    media_bundles = [],
    slug = ""

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
        return u"(location={}, title={}, subtitle={}, media_bundles={}, slug={})".format(self.location, self.title,
                                                                                         self.subtitle,
                                                                                         self.media_bundles, self.slug)
    # end __unicode__

    def __str__(self):
        """
        To unicode
        :return:
        """
        return "(location={}, title={}, subtitle={}, media_bundles={}, slug={})".format(str(self.location), self.title,
                                                                                        self.subtitle.encode('ascii', 'ignore'),
                                                                                        self.media_bundles, self.slug)
    # end __unicode__

# end Media
