#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Imports
from .FollowersCursor import FollowersCursor


# Following cursor
class FollowingCursor(FollowersCursor):
    """
    Following cursor
    """

    # URLs
    _edge = 'edge_follow'
    _referer = 'https://www.instagram.com/{}/following/'

# end FollowingCursor
