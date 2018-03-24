#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import skimage
import skimage.io
import argparse
import torch
import torch.nn as nn
from Net import Net
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
from torch.autograd import Variable

border_size = 50
window_size = border_size * 2 + 1

# Load images
original_image = skimage.io.imread("castle.jpg")
hdr_image = skimage.io.imread("castle_hdr.jpg")

# Image size
image_width = original_image.shape[0]
image_height = original_image.shape[1]

# Image
image = np.zeros((image_width + border_size * 2, image_height + border_size * 2, 3))
image[border_size:border_size+image_width, border_size:border_size+image_height] = original_image


