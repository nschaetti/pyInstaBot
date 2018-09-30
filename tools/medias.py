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
import skimage.transform
from PIL import Image
from PIL.ExifTags import TAGS
import math
import logging
import strings as pystr
import numpy as np


# Rotate picture
def rotate_picture(path_to_image):
    """
    Rotate picture to its original angle.
    :param path_to_image:
    :return:
    """
    # Transformation
    rotation = 0.0
    vertical_flip = False
    horizontal_flip = False
    orientation = 1

    # Get orientation
    try:
        for (k, v) in Image.open(path_to_image)._getexif().iteritems():
            if TAGS.get(k) == "Orientation":
                orientation = v
            # end if
        # end for
    except AttributeError:
        return
    # end try

    # Get transformation
    if orientation == 2:
        vertical_flip = True
    elif orientation == 3:
        rotation = 2
    elif orientation == 4:
        rotation = 2
        vertical_flip = True
    elif orientation == 5:
        rotation = 3
        horizontal_flip = True
    elif orientation == 6:
        rotation = 3
    elif orientation == 7:
        rotation = 3
        vertical_flip = True
    elif orientation == 8:
        rotation = 1
    # end if

    # Load image
    im = skimage.io.imread(path_to_image)

    # Apply rotation
    if rotation != 0.0:
        # im = skimage.transform.rotate(im, rotation)
        im = np.rot90(im, rotation)
    # end if

    # Apply horizontal flip
    if horizontal_flip:
        im = im[:, ::-1]
    # end if

    # Apply vertical flip
    if vertical_flip:
        im = im[::-1, :]
    # end if

    # Save
    logging.getLogger(pystr.LOGGER).info(u"Changing orientation of {}".format(path_to_image.decode('utf-8', errors='ignore')))
    skimage.io.imsave(path_to_image, im)
# end rotate_picture


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
