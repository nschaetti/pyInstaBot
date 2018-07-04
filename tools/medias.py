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


# Reframe a picture to be compatible with Instagram
def reframe_picture(path_to_image):
    """
    Reframe a picture to be compatible with Instagram.

    Arguments:
        path_to_image (str): Path to the image to reframe.
    """
    print(path_to_image)
    # Load image
    im = skimage.io.imread(path_to_image)

    # Size
    height = im.shape[0]
    width = im.shape[1]

    # Portrait or landscape
    if height > width:
        # Height for 4:5
        new_height = int(math.ceil(width * 1.25))

        # Apply if ok
        if new_height < height:
            # Size
            new_height_half = int(new_height / 2.0)

            # New image
            im = im[new_height_half:-new_height_half, :]
        else:
            # New width
            new_width = int(math.ceil(height * 0.8))

            # Size
            new_width_half = int(new_width / 2.0)

            # New image
            im = im[:, new_width_half:-new_width_half]
        # end if
    else:
        # Width for 1.91:1
        new_width = int(math.ceil(height * 1.91))

        # Apply if ok
        if new_width < width:
            # Size
            new_width_half = int(new_width / 2.0)

            # New image
            im = im[:, new_width_half:-new_width_half]
        else:
            # New height
            new_height = int(math.ceil(width * 0.5235602094))

            # Size
            new_height_half = int(new_height / 2.0)

            # New image
            im = im[new_height_half:-new_height_half, :]
        # end if
    # end if

    # Save
    print(u"Saving to {}".format(path_to_image))
    skimage.io.imsave(path_to_image, im)
    exit()
# end reframe_picture
