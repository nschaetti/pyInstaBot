#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Import
import logging
from executor.ActionScheduler import ActionReservoirFullError, ActionAlreadyExists
from media.MediaFinder import MediaFinder
from  textblob import TextBlob
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
def find_medias(config, model_file, action_scheduler, min_length=50, threshold=0.5):
    """

    :param config:
    :param model_file:
    :param action_scheduler:
    :param threshold:
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
        for media in MediaFinder(search_keywords=hashtag, shuffle=True):
            # Media's caption
            media_caption = media['caption']['text']
            media_id = media['pk']

            # Predict class
            censor_prediction, _ = censor(media_caption)

            # Debug
            logging.getLogger(pystr.LOGGER).debug(
                pystr.DEBUG_NEW_MEDIA_FOUND.format(hashtag, media_id)
            )

            # TextBlob
            media_text_blob = TextBlob(media_caption)
            print(media_text_blob.detect_language())
            # Pass the censor
            if len(media_caption) > min_length and censor_prediction == 'pos' and media_text_blob.detect_language() in \
                    config.post['languages']:
                # Comment
                comment = u"Nice!"

                # Try to add
                try:
                    logging.getLogger(pystr.LOGGER).info(pystr.INFO_ADD_COMMENT_SCHEDULER.format(
                        comment,
                        media_id
                    ))
                    action_scheduler.add_comment(media_id, comment)
                except ActionReservoirFullError:
                    logging.getLogger(pystr.LOGGER).error(pystr.ERROR_RESERVOIR_FULL)
                    exit()
                    pass
                except ActionAlreadyExists:
                    logging.getLogger(pystr.LOGGER).error(pystr.ERROR_COMMENT_ALREADY_DB.format(
                        media_id.encode('ascii', errors='ignore')))
                    pass
                # end try
        # end for
    # end for
# end
