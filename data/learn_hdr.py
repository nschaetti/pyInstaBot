#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import skimage
import skimage.io
import argparse

# Parser
parser = argparse.ArgumentParser(prog='Learn HDR')
parser.add_argument("--output", type=str, required=True)

# Load images
image = skimage.io.imread("castle.jpg")

