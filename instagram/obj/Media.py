#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


# A Media
class Media(object):

    # Properties
    id = 0,
    typename = '',
    edge_media_to_caption = {},
    shortcode = '',
    edge_media_to_comment = {},
    comments_disabled = False,
    taken_at_timestamp = 0,
    dimensions = {},
    display_url = u"",
    edge_media_preview_like = {},
    owner = {},
    thumbnail_src = u"",
    thumbnail_resources = [],
    is_video = False

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
        return u"(id={}, typename={}, edge_media_to_caption={}, shortcode={}, edge_media_to_comment={}, " \
               u"comments_disabled={}, taken_at_timestamp={}, dimensions={}, display_url={}, " \
               u"edge_media_preview_like={}, owner={}, thumbnail_src={}, thumbnail_resources={}, is_video={})"\
            .format(self.id, self.typename, self.edge_media_to_caption, self.shortcode, self.edge_media_to_comment,
                    self.comments_disabled, self.taken_at_timestamp, self.dimensions, self.display_url,
                    self.edge_media_preview_like, self.owner, self.thumbnail_src, self.thumbnail_resources,
                    self.is_video)
    # end __unicode__

    def __str__(self):
        """
        To unicode
        :return:
        """
        return "(id={}, typename={}, edge_media_to_caption={}, shortcode={}, edge_media_to_comment={}, " \
               "comments_disabled={}, taken_at_timestamp={}, dimensions={}, display_url={}, " \
               "edge_media_preview_like={}, owner={}, thumbnail_src={}, thumbnail_resources={}, is_video={})"\
            .format(self.id, self.typename, self.edge_media_to_caption, self.shortcode, self.edge_media_to_comment,
                    self.comments_disabled, self.taken_at_timestamp, self.dimensions, self.display_url,
                    self.edge_media_preview_like, self.owner, self.thumbnail_src, self.thumbnail_resources,
                    self.is_video)
    # end __unicode__

# end Media
