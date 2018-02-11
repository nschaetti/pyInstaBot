#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : __init__.py
# Description : Main init file.
# Auteur : Nils Schaetti <n.schaetti@gmail.com>
# Date : 11.02.2018 13:51:05
# Lieu : Nyon, Suisse
#
# This file is part of the pyInstaBot.
# The pyInstaBot is a set of free software:
# you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyTweetBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with pyTweetBar.  If not, see <http://www.gnu.org/licenses/>.
#

# Import
import argparse
import logging
import sys
import time
import pkg_resources
import tools.strings as pystr
from instagram.Instagram import Instagram
from db.DBConnector import DBConnector
from config.BotConfig import BotConfig, MissingRequiredField
from create_database import create_database
import codecs


####################################################
# Functions
####################################################


# Add default arguments
def add_default_arguments(p):
    """
    Add default arguments
    :param parser:
    :return:
    """
    # Configuration and log
    p.add_argument("--config", type=str, help="Configuration file", required=True)
    p.add_argument("--log-level", type=int, help="Log level", default=20)
    p.add_argument("--log-file", type=str, help="Log file", default="")
# end add_default_arguments


# Create logger
def create_logger(name, log_level=logging.INFO, log_format="%(asctime)s :: %(levelname)s :: %(message)s", log_file=""):
    """
    Create logger
    :param name: Logger's name
    :param log_level: Log level
    :param log_format: Log format
    :param log_file: Where to put the logs
    :return: The logger object
    """
    # New logger
    logging.basicConfig()
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Create a file handler if needed
    if log_file != "":
        handler = logging.FileHandler(log_file)
        handler.setLevel(log_level)

        # Create a logging format
        formatter = logging.Formatter(log_format)
        handler.setFormatter(formatter)

        # Add the handlers to the logger
        logger.addHandler(handler)
    # end if

    return logger
# end create_logger


# Create config file
def create_config(config_filename):
    """
    Create config file
    :param config_filename:
    :return:
    """
    # Get template
    empty_config = pkg_resources.resource_string("pyInstaBot.config", 'config.json')

    # Write
    file_handler = codecs.open(config_filename, 'w', encoding='utf-8')
    file_handler.write(unicode(empty_config) + u"\n")
    file_handler.close()
# end create_config


####################################################
# Main function
####################################################


if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(prog="pyInstaBot",
                                     description="pyInstaBot - A smart Instagram bot to replace yourself")

    # Command sub parser
    command_subparser = parser.add_subparsers(dest="command")

    # Database parser
    tools_parser = command_subparser.add_parser("tools")
    add_default_arguments(tools_parser)
    tools_parser.add_argument("--create-database", action='store_true',
                              help="Create the database structure on the MySQL host", default=False)
    tools_parser.add_argument("--create-config", action='store_true',
                              help="Create an empty configuration file", default=False)

    # Learning
    learning_parser = command_subparser.add_parser("learning")
    learning_parser.add_argument("--task", type=str, help="Task to learn (post, like, comment, follow)")
    learning_parser.add_argument("--gui", action='store_true', help="Show graphical user interface", default=False)
    learning_parser.add_argument("--output", type=str, help="Output file where to store the dataset", required=True)
    add_default_arguments(learning_parser)

    # Parse
    args = parser.parse_args()

    # Logging
    logger = create_logger(pystr.LOGGER, log_level=args.log_level, log_file=args.log_file)

    # Need config and connect?
    if args.command != "tools" or not args.create_config:
        # Load configuration file
        try:
            config = BotConfig.load(args.config)
        except MissingRequiredField as e:
            sys.stderr.write(pystr.ERROR_PARSING_CONFIG_FILE.format(e))
            exit()
        # end try

        # Connection to MySQL
        dbc = config.database
        mysql_connector = DBConnector(host=dbc["host"], username=dbc["username"], password=dbc["password"],
                                      db_name=dbc["database"])

        # Login to Instagram
        instagram = Instagram(user_id=config.instagram['user_id'], username=config.instagram['username'],
                              password=config.instagram['password'])
        instagram.login()
        time.sleep(1)
    # end if

    # Different possible command
    if args.command == "tools":
        # Create database
        if args.create_database:
            create_database(config)
        elif args.create_config:
            create_config(args.config)
        # end if
    else:
        sys.stderr.write(pystr.ERROR_UNKNOWN_COMMAND.format(args.command))
    # end if

    """users, places, hashtags = instagram.search("blender")
    for hashtag in hashtags:
        print(hashtag)
    # end for

    # Test
    for media in Cursor(instagram.home_timeline):
        print(media)
    # end for

    # For each follower
    for user in instagram.following():
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

    # instagram.logout()

# end if
