#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Imports
import time
import logging
import argparse
from db.DBConnector import DBConnector
from instagram.Instagram import Instagram
from gui.ImageClassificationWindow import ImageClassificationWindow

#########################################
# Functions
#########################################

# Add default arguments
def add_default_arguments(p):
    """
    Add default arguments
    :param p: Parser object
    :return:
    """
    # Configuration and log
    p.add_argument("--config", type=str, help="Configuration file", required=True)
    p.add_argument("--log-level", type=int, help="Log level", default=20)
    p.add_argument("--log-file", type=str, help="Log file", default="")
# end add_default_arguments

#########################################
# Main function
#########################################

if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser(prog="pyInstaBot",
                                     description="pyInstaBot - A smart bot with a little bit of Computer Vision to replace yourself on Instagram")

    # Command subparser
    command_subparser = parser.add_subparsers(dest="command")

    # Learning
    learning_parser = command_subparser.add_parser("learning")
    learning_parser.add_argument("--task", type=str, help="Task to learn (post, like, comment, follow)")
    learning_parser.add_argument("--gui", action='store_true', help="Show graphical user interface", default=False)
    learning_parser.add_argument("--output", type=str, help="Output file where to store the dataset", required=True)
    add_default_arguments(learning_parser)

    # Parse
    args = parser.parse_args()

    # Logging
    logging.basicConfig(level=20, format='%(asctime)s :: %(levelname)s :: %(message)s')

    # Connection to MySQL
    mysql_connector = DBConnector(host="localhost", username="root", password="1234", db_name="nilsbot")

    # Test command
    # Update statistics
    if args.command == "learning":
        # Which task
        if args.task == "post":
            window = ImageClassificationWindow()
            window.show()
        # end if
    # Find tweets

    instagram = Instagram(user_id=2926312088, username="n.schaetti.public", password="oB4JLE02YDbfB9uBlAaG")

    instagram.login()

    time.sleep(2)

    users, places, hashtags = instagram.search("blender")
    for hashtag in hashtags:
        print(hashtag)
    # end for"""

    # Test
    """for media in Cursor(instagram.home_timeline):
        print(media)
    # end for"""

    # For each follower
    """for user in instagram.following():
        if not User.exists(user.user_id):
            logging.getLogger(u"pyInstaBot").info(u"New following in the database : {}".format(user))

            # Following
            user.user_is_following = True
            user.user_following_date = datetime.datetime.utcnow()

            # Add to DB
            mysql_connector.get_session().add(user)
        elif not User.get(user.user_id).is_following():
            # Update
            user.user_is_following = True
            user.user_following_date = datetime.datetime.utcnow()
        # end if

        # Commit
        mysql_connector.get_session().commit()
        # end for

    # For each follower
    for user in instagram.followers():
        if not User.exists(user.user_id):
            logging.getLogger(u"pyInstaBot").info(u"New follower in the database : {}".format(user))

            # Follower
            user.user_is_follower = True
            user.user_follower_date = datetime.datetime.utcnow()

            # Add to DB
            mysql_connector.get_session().add(user)
        elif not User.get(user.user_id).is_follower():
            # Update
            user.user_is_follower = True
            user.user_follower_date = datetime.datetime.utcnow()
        # end if

        # Commit
        mysql_connector.get_session().commit()
    # end for

    time.sleep(2)"""

    instagram.logout()
# end if
