#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Imports
import time
import logging
import datetime
from db.DBConnector import DBConnector
from instagram.Instagram import Instagram
from db.obj.User import User
from instagram.Cursor import Cursor


if __name__ == "__main__":
    # Logging
    logging.basicConfig(level=20, format='%(asctime)s :: %(levelname)s :: %(message)s')

    # Connection to MySQL
    mysql_connector = DBConnector(host="localhost", username="", password="", db_name="")

    instagram = Instagram(user_id=, username="", password="")

    instagram.login()

    time.sleep(2)

    for media in Cursor(instagram.user_timeline):
        print(media)
    # end for

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
