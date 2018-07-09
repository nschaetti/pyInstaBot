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

# Imports
import skimage.io
import math
import logging
import tools.strings as pystr


# Reframe a picture to be compatible with Instagram
def reframe_picture(path_to_image):
    """
    Reframe a picture to be compatible with Instagram.

    Arguments:
        path_to_image (str): Path to the image to reframe.
    """
    # Load image
    im = skimage.io.imread(path_to_image)

    # Size
    height = float(im.shape[0])
    width = float(im.shape[1])

    # Portrait or landscape
    if height > width:
        # Check ratio
        if round(height / width, 2) == 1.25:
            return
        # end if

        # Height for 4:5
        new_height = int(math.ceil(width * 1.25))

        # Apply if ok
        if new_height < height:
            # Size
            padding_half = int((height - new_height) / 2.0)

            # New image
            im = im[padding_half:-padding_half-1, :]
        else:
            # New width
            new_width = int(math.ceil(height * 0.8))

            # Size
            padding_half = int((width - new_width) / 2.0)

            # New image
            im = im[:, padding_half:-padding_half-1]
        # end if
    else:
        # Check ratio
        if round(width / height, 2) == 1.91:
            return
        # end if

        # Width for 1.91:1
        new_width = int(math.ceil(height * 1.91))

        # Apply if ok
        if new_width < width:
            # Size
            padding_half = int((width - new_width) / 2.0)

            # New image
            im = im[:, padding_half:-padding_half-1]
        else:
            # New height
            new_height = int(math.ceil(width * 0.5235602094))

            # Size
            padding_half = int((height - new_height) / 2.0)

            # New image
            im = im[padding_half:-padding_half-1, :]
        # end if
    # end if

    # Save
    logging.getLogger(pystr.LOGGER).info(u"Changing aspect ratio of {}".format(path_to_image.decode('utf-8', errors='ignore')))
    skimage.io.imsave(path_to_image, im)
# end reframe_picture
