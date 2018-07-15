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
import pkg_resources
import tools.strings as pystr
import friends
from executor.ActionScheduler import ActionScheduler
from db.DBConnector import DBConnector
from config.BotConfig import BotConfig, MissingRequiredField
from execute_actions import execute_actions
from create_database import create_database
from instagram.InstagramConnector import InstagramConnector
import codecs
from .add_medias import add_medias
from .apply_filter import apply_filter
from .find_follows import find_follows
from .find_medias import find_medias
from .find_unfollows import find_unfollows
from .find_locations import find_locations


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
    p.add_argument("--session", type=str, help="Session file", required=True)
    p.add_argument("--config", type=str, help="Configuration file", required=True)
    p.add_argument("--log-level", type=int, help="Log level", default=20)
    p.add_argument("--log-file", type=str, help="Log file", default="")
# end add_default_arguments


# Add model argument
def add_model_argument(p, required):
    """
    Add model argument
    :param p: Parser object
    :param required: Is the model argument required?
    """
    # Model
    p.add_argument("--model", type=str, help="Classification model's file", required=required)
    p.add_argument("--threshold", type=float, help="Probability threshold for the prediction to be positive",
                   default=0.5, required=False)
# end add_model_argument


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

    # Find follow
    find_follow_parser = command_subparser.add_parser("find-follows")
    add_default_arguments(find_follow_parser)
    add_model_argument(find_follow_parser, True)
    find_follow_parser.add_argument("--text-size", type=int,
                                    help="Minimum test size to take into account for the test",
                                    default=50)

    # Find unfollow
    find_unfollow_parser = command_subparser.add_parser("find-unfollows")
    add_default_arguments(find_unfollow_parser)
    add_model_argument(find_unfollow_parser, True)

    # Find comments
    find_comments_parser = command_subparser.add_parser("find-comments")
    add_default_arguments(find_comments_parser)
    add_model_argument(find_comments_parser, True)

    # Find likes
    find_likes_parser = command_subparser.add_parser("find-likes")
    add_default_arguments(find_likes_parser)
    add_model_argument(find_likes_parser, True)

    # Find locations
    find_locations_parser = command_subparser.add_parser("find-locations")
    add_default_arguments(find_locations_parser)
    find_locations_parser.add_argument("--location", type=str, help="Location term to search")
    add_model_argument(find_locations_parser, True)

    # List and update followers/friends list
    list_friends_parser = command_subparser.add_parser("friends")
    add_default_arguments(list_friends_parser)
    list_friends_parser.add_argument("--update", action='store_true', help="Update followers/friends in the DB")
    list_friends_parser.add_argument("--obsolete", action='store_true', help="Show only obsolete friends")
    list_friends_parser.add_argument("--friends", action='store_true', help="Show only friends")

    # Executor
    executor_parser = command_subparser.add_parser("execute")
    add_default_arguments(executor_parser)
    executor_parser.add_argument("--daemon", action='store_true', help="Run executor in daemon mode", default=False)
    executor_parser.add_argument("--break-time", action='store_true',
                                 help="Show break duration between execution for the current time", default=False)

    # Add medias
    medias_parser = command_subparser.add_parser("medias")
    add_default_arguments(medias_parser)
    medias_parser.add_argument("--add", type=str, help="A directory of medias or a file to add")
    medias_parser.add_argument("--caption", type=str, help="The media's caption")
    medias_parser.add_argument("--fitler", type=str, help="Filter (none, andromeda, chicago, geneva, ghost, sanfrancisco, sixties, sunnydays, random")
    medias_parser.add_argument("--hashtags", type=str, help="List of filters to add separated by comma")
    medias_parser.add_argument("--album", action='store_true', help="Create an album with the medias", default=False)
    medias_parser.add_argument("--loop", action='store_true', help="Post medias again and again", default=False)

    # Apply filters
    filters_parser = command_subparser.add_parser("filters")
    add_default_arguments(filters_parser)
    filters_parser.add_argument("--input", type=str, help="Path to input image")
    filters_parser.add_argument("--output", type=str, help="Path to output image")
    filters_parser.add_argument("--filter", type=str,
                               help="Filter (none, andromeda, chicago, geneva, ghost, sanfrancisco, sixties, sunnydays")

    # Parse
    args = parser.parse_args()

    # Logging
    logger = create_logger(pystr.LOGGER, log_level=args.log_level, log_file=args.log_file)

    # Instagram connector
    instagram = None

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
        
        # Login instagram
        instagram_connector = InstagramConnector(args.session, config)

        # Friends manager
        friends_manager = friends.FriendsManager(instagram)

        # Action scheduler
        action_scheduler = ActionScheduler(config=config)
    # end if

    # Different possible command
    if args.command == "medias":
        add_medias(config, args.add, args.caption, action_scheduler, args.album, args.loop)
    # Find follows
    elif args.command == "find-follows":
        find_follows(config, args.model, action_scheduler, args.text_size)
    # Find unfollows
    elif args.command == "find-unfollows":
        find_unfollows(config, action_scheduler, friends_manager, args.model)
    # Find comments
    elif args.command == "find-comments":
        find_medias(instagram_connector, config, args.model, action_scheduler, 'comment', args.threshold)
    # Find likes
    elif args.command == "find-likes":
        find_medias(instagram_connector, config, args.model, action_scheduler, 'like', args.threshold)
    # Find locations
    elif args.command == "find-locations":
        find_locations(instagram_connector, config, args.location)
    elif args.command == "tools":
        # Create database
        if args.create_database:
            create_database(config)
        elif args.create_config:
            create_config(args.config)
        # end if
    # Executor
    elif args.command == "execute":
        execute_actions(config, action_scheduler)
    # List friends
    elif args.command == "friends":
        # Update friends
        if args.update:
            friends_manager.update()
        # end if
    # Apply filter to an image
    elif args.command == "filter":
        apply_filter(args.input, args.output, args.fitler)
    else:
        sys.stderr.write(pystr.ERROR_UNKNOWN_COMMAND.format(args.command))
    # end if

    if instagram is not None and instagram.isLoggedIn:
        instagram.logout()
    # end if

# end if
