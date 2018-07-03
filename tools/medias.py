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

    # Portrait or landscape
    if im.shape[0] > im.shape[1]:
        print(u"Paysage")
    else:
        print(u"Portrait")
    # end if
    print(im)
    print(type(im))
    exit()
# end reframe_picture
