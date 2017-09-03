#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Imports
import time
import logging
from instagram.Instagram import Instagram


if __name__ == "__main__":
    # Logging
    logging.basicConfig(level=20, format='%(asctime)s :: %(levelname)s :: %(message)s')

    instagram = Instagram(username="", password="")

    instagram.login()

    time.sleep(2)

    instagram.logout()
# end if
