#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Imports
from Tkinter import *


# Image classification window
class ImageClassificationWindow(object):

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        # Create main window
        self._main_window = Tk()

        # Compose the GUI
        self._compose()
    # end __init__

    #######################################
    # Public
    #######################################

    # Show window
    def show(self):
        """
        Show window
        :return:
        """
        self._main_window.mainloop()
    # end show

    #######################################
    # Private
    #######################################

    # Compose GUI
    def _compose(self):
        """
        Compose GUI
        :return:
        """
        w = Label(self._main_window, text="Coucou").pack(fill=X)
    # end compose

# end ImageClassificationWindow
