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
            # Media's caption
            user_name = user['username']
            user_bio = user['biography']
            user_id = user['pk']

            # Predict class
            censor_prediction, _ = censor(user_bio)

            # Debug
            logging.getLogger(pystr.LOGGER).debug(
                pystr.DEBUG_NEW_USER_FOUND.format(hashtag, user_name)
            )

            # TextBlob
            media_text_blob = TextBlob(user_bio)

            # Pass the censor
            if len(user_bio) > min_length and censor_prediction == 'pos' and media_text_blob.detect_language() in \
                    config.post['languages']:
                # Try to add
                try:
                    # Add action
                    logging.getLogger(pystr.LOGGER).info(pystr.INFO_ADD_FOLLOW_SCHEDULER.format(
                        user_name
                    ))
                    action_scheduler.add_follow(user_id)
                except ActionReservoirFullError:
                    logging.getLogger(pystr.LOGGER).error(pystr.ERROR_RESERVOIR_FULL)
                    exit()
                    pass
                except ActionAlreadyExists:
                    logging.getLogger(pystr.LOGGER).error(pystr.ERROR_FOLLOW_ALREADY_DB.format(
                        user_name))
                    pass
                # end try
            # end if
        # end for
    # end for
# end
