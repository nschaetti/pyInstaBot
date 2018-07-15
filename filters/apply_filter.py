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
import tools.strings as pystr
import skimage
import skimage.io
from filters import *
import logging
import tools.strings as pystr


# Filters
filters = ["none", "geneva"]


# Apply filter
def apply_filter(image_path, filter):
    """
    Apply filter
    :param input:
    :param filter:
    :return:
    """
    # Output path
    file_ext =  os.path.splitext(image_path)[1]
    output_path = os.path.splitext(image_path)[0] + "_" + filter + file_ext

    # Check if already done
    if os.path.exists(output_path):
        return output_path
    # end if

    # None
    if filter == "none":
        return image_path
    # end if"

    # Log
    logging.getLogger(pystr.LOGGER).info(u"Applying filter {} to {}".format(filter, image_path))

    # Load image
    img = skimage.io.imread(image_path)

    # Filter function
    img = geneva(img, {})

    # Save image
    skimage.io.imsave(output_path, img)

    return output_path
# end apply_filter

