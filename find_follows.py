#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Import
import logging
from executor.ActionScheduler import ActionReservoirFullError, ActionAlreadyExists
from friends.FriendsFinder import FriendsFinder
from  textblob import TextBlob
import learning
import tools.strings as pystr

####################################################
# Globals
####################################################


####################################################
# Functions
####################################################


####################################################
# Main function
####################################################


# Find new Instagram users to follow
def find_follows(config, model_file, action_scheduler, min_length=50):
    """
    Find new medias from various sources
    :param config:
    :param model_file:
    :param action_scheduler:
    :param min_length:
    :return:
    """
    # Load censor
    censor = learning.CensorModel.load_censor(config)

    # Load model
    """if os.path.exists(model_file):
        model = pickle.load(open(model_file, 'rb'))
    else:
        logging.getLogger(pystr.LOGGER).error(u"Cannot find model {}".format(model_file))
        exit()
    # end if

    # Mode loaded
    logging.getLogger(pystr.LOGGER).info(u"Model {} loaded".format(model_file))"""

    # For each tags
    for hashtag in config.hashtags:
        # For each media
        for user in FriendsFinder(hashtag=hashtag, shuffle=True):
            # User
            print(user)
        # end for
    # end for
# end
