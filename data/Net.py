#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Imports
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F


# FFNN
class Net(nn.Module):
    """
    FFNN
    """

    # Constructor
    def __init__(self, image_size, hidden_size=100, n_channels=3):
        """
        Constructor
        """
        super(Net, self).__init__()
        self.image_size = image_size
        self.n_channels = n_channels
        self.linear1 = nn.Linear(image_size * image_size * n_channels, hidden_size)
        self.linear2 = nn.Linear(hidden_size, n_channels)
    # end __init__

    # Forward pass
    def forward(self, x):
        """
        Forward pass
        :param x:
        :return:
        """
        x = F.sigmoid(self.linear1(x.view(-1, self.image_size * self.image_size * self.n_channels)))
        return self.linear2(x)
    # end forward

# end Net
