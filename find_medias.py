#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Import
import logging
from executor.ActionScheduler import ActionReservoirFullError, ActionAlreadyExists
from media.MediaFinder import MediaFinder
import instagram
import learning
import media as md
import tools.strings as pystr
import pickle
import os

####################################################
# Globals
####################################################


####################################################
# Functions
####################################################


####################################################
# Main function
####################################################


# Find new medias from various sources
def find_medias(config, model_file, action_scheduler, threshold=0.5):
    """

    :param config:
    :param model_file:
    :param action_scheduler:
    :param threshold:
    :return:
    """
    # Media finder
    # media_finder = MediaFinder(shuffle=True)

    # Load censor
    """censor = learning.CensorModel.load_censor(config)

    # Load model
    if os.path.exists(model_file):
        model = pickle.load(open(model_file, 'rb'))
    else:
        logging.getLogger(pystr.LOGGER).error(u"Cannot find model {}".format(model_file))
        exit()
    # end if

    # Mode loaded
    logging.getLogger(pystr.LOGGER).info(u"Model {} loaded".format(model_file))"""

    # For each tags
    for hashtag in config.hashtags:
        # Get hashtag feed
        hashtag_feed = instagram.InstagramConnector().hashtag_feed(hashtag)
        print(hashtag_feed)
    # end for
# end
