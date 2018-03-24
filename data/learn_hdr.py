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

# Settings
n_epoch = 3
batch_size = 400
border_size = 50
window_size = border_size * 2 + 1

# Parser
parser = argparse.ArgumentParser(prog='Learn HDR')
parser.add_argument("--output", type=str, required=True)

# Load images
original_image = skimage.io.imread("castle.jpg")
hdr_image = skimage.io.imread("castle_hdr.jpg")

# Image size
image_width = original_image.shape[0]
image_height = original_image.shape[1]

# Image
image = np.zeros((image_width + border_size * 2, image_height + border_size * 2, 3))
image[border_size:border_size+image_width, border_size:border_size+image_height] = original_image

# Neural net
net = Net(window_size, hidden_size=300)

# MSE loss
criterion = nn.MSELoss()

# Learning rate
learning_rate = 0.0001

# SGD
optimizer = optim.SGD(net.parameters(), lr=learning_rate, momentum=0.9)

# For each iteration
for epoch in range(n_epoch):
    # Index
    index = 0

    # Loss
    average_loss = 0.0
    total = 0.0

    # For each pixel
    for x in np.arange(border_size, border_size+image_width):
        for y in np.arange(border_size, border_size+image_height):
            # New batch
            if index == 0:
                batch = torch.zeros(batch_size, 3, window_size, window_size)
                outputs = torch.zeros(batch_size, 3)
            # end if

            # Position
            start_x = x - border_size
            start_y = y - border_size
            end_x = x + 1 + border_size
            end_y = y + 1 + border_size

            # Get pixels
            pixels = torch.FloatTensor(image[start_x:end_x, start_y:end_y])
            batch[index] = torch.transpose(pixels, dim0=0, dim1=2)
            outputs[index] = torch.FloatTensor(hdr_image[x-border_size, y-border_size])

            # Batch
            if index == batch_size - 1:
                # To variable
                inputs, outputs = Variable(batch), Variable(outputs)

                # Gradients to zero
                optimizer.zero_grad()

                # Forward
                net_outputs = net(inputs)

                # Loss
                loss = criterion(net_outputs, outputs)

                # Backward
                loss.backward()

                # Optimize
                optimizer.step()

                # Add loss
                average_loss += loss.data[0]
                total += 1.0

                # Index
                index = 0
            else:
                index += 1
            # end if
        # end for
    # end for

    # Show average
    print(u"Loss : {}".format(average_loss / total))
# end for

torch.save(net, open("net.p", "wb"))
