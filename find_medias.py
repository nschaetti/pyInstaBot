#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Import
import logging
from executor.ActionScheduler import ActionReservoirFullError, ActionAlreadyExists
from media.MediaFinder import MediaFinder
import langdetect.lang_detect_exception
import learning
import tools.strings as pystr
import random
from langdetect import detect
from pyInstaBot.db.obj.Comment import Comment


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
def find_medias(instagram_connector, config, model_file, action_scheduler, action='comment', min_length=50, threshold=0.5):
    """
    Find new medias from various sources
    :param config:
    :param model_file:
    :param action_scheduler:
    :param action:
    :param min_length:
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
            if media is not None and media['caption'] is not None:
                # Media's caption
                media_code = media['code']
                media_caption = media['caption']['text']
                media_id = media['pk']
                media_username = media['user']['username']
                print(instagram_connector.media_info(media_id))
                exit()
                # Predict class
                censor_prediction, _ = censor(media_caption)

                # Debug
                logging.getLogger(pystr.LOGGER).debug(
                    pystr.DEBUG_NEW_MEDIA_FOUND.format(hashtag, media_id)
                )

                # Pass the censor
                try:
                    if len(media_caption) > min_length and censor_prediction == 'pos' and detect(media_caption) in config.post['languages']:
                        # Select random comment
                        comment = random.choice(config.post['comments'])

                        # Try to add
                        try:
                            # Add action
                            if action == 'comment':
                                if Comment.exists_media(media_id) or Comment.exists_username(comment, media_username):
                                    logging.getLogger(pystr.LOGGER).info(u"Same comment for username {} or comment for media {} already exists".format(media_username, media_id))
                                else:
                                    logging.getLogger(pystr.LOGGER).info(pystr.INFO_ADD_COMMENT_SCHEDULER.format(
                                        comment,
                                        media_id,
                                        media_code
                                    ))
                                    action_scheduler.add_comment(media_id, comment, media_code, media_username)
                                # end if
                            else:
                                logging.getLogger(pystr.LOGGER).info(pystr.INFO_ADD_LIKE_SCHEDULER.format(
                                    media_id,
                                    media_code
                                ))
                                action_scheduler.add_like(media_id, media_code)
                            # end if
                        except ActionReservoirFullError:
                            logging.getLogger(pystr.LOGGER).error(pystr.ERROR_RESERVOIR_FULL)
                            exit()
                            pass
                        except ActionAlreadyExists:
                            logging.getLogger(pystr.LOGGER).error(pystr.ERROR_COMMENT_ALREADY_DB.format(
                                media_id))
                            pass
                        # end try
                    # end if
                except langdetect.lang_detect_exception.LangDetectException:
                    pass
                # end try
            # end if
        # end for
    # end for
# end
