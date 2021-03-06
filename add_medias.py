#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : pyTweetBot.py
# Description : pyTweetBot main execution file.
# Auteur : Nils Schaetti <n.schaetti@gmail.com>
# Date : 01.05.2017 17:59:05
# Lieu : Nyon, Suisse
#
# This file is part of the pyTweetBot.
# The pyTweetBot is a set of free software:
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
import os
import logging
from moviepy.editor import *
import tools.strings as pystr
import tools.medias as med
import executor.ActionScheduler
import codecs


# Add media
def add_medias(instagram_connector, config, directory_path, caption_file, action_scheduler, is_album, action_loop, location="", filter="none"):
    """
    Add medias from directory or file
    :param directory_path:
    :param caption:
    :return:
    """
    # Load caption from file
    caption = codecs.open(caption_file, 'r', encoding='utf-8').read()

    # Additional caption
    add_caption = config.post['caption']

    # List directory
    if os.path.isdir(directory_path):
        # List dir
        for file_path in os.listdir(directory_path):
            # If jpeg
            if ".jpg" in file_path or ".jpeg" in file_path:
                # Rotate image to its original angle
                med.rotate_picture(os.path.join(directory_path, file_path))

                # Make sure it is compatible with Instagram
                med.reframe_picture(os.path.join(directory_path, file_path))

                # Add post
                try:
                    action_scheduler.add_post(os.path.join(directory_path, file_path), u"", caption + add_caption, location, action_loop, filter)
                except executor.ActionScheduler.ActionAlreadyExists:
                    logging.getLogger(pystr.LOGGER).error(u"Action already in the database")
                # end try"
            elif ".mp4" in file_path:
                # Thumbnail path
                thumbnail_path = os.path.join(directory_path, file_path).decode('utf-8')
                thumbnail_path = thumbnail_path[:-4] + u"_thumbnail.jpeg"

                # Create thumbnail
                clip = VideoFileClip(os.path.join(directory_path, file_path))
                clip.save_frame(thumbnail_path, 0.0)

                # Add post
                try:
                    action_scheduler.add_post(os.path.join(directory_path, file_path), thumbnail_path, caption + add_caption, location, action_loop)
                except executor.ActionScheduler.ActionAlreadyExists:
                    logging.getLogger(pystr.LOGGER).error(u"Action already in the database")
                # end try
            else:
                logging.getLogger(pystr.LOGGER).warning(u"File {} is not a supported format (jpeg, mp4), rejected".format(file_path))
            # end if
        # end for
    else:
        # If jpeg
        if ".jpg" in directory_path or ".jpeg" in directory_path:
            # Rotate image to its original angle
            med.rotate_picture(directory_path)

            # Make sure it is compatible with Instagram
            med.reframe_picture(directory_path)

            # Add post
            try:
                action_scheduler.add_post(directory_path, u"", caption + add_caption, action_loop, filter)
            except executor.ActionScheduler.ActionAlreadyExists:
                logging.getLogger(pystr.LOGGER).error(u"Action already in the database")
            # end try
        else:
            logging.getLogger(pystr.LOGGER).warning(u"File {} is not a supported format (jpeg, mp4), rejected".format(directory_path))
        # end if
    # end if
# end add_medias
