#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/26 上午10:10
# @Site    : 
# @File    : model.py
# @Software: PyCharm
import paddle
import paddle.nn as nn
import paddle.nn.functional as F
import parl


class CartpoleModel(parl.Model):
    """ Linear network to solve Cartpole problem.
        Args:
            obs_dim (int): Dimension of observation space.
            act_dim (int): Dimension of action space.
        """

    def __init__(self, obs_dim, act_dim):
        super(CartpoleModel, self).__init__()
        hid1_size = 128
        hid2_size = 128
        self.fc1 = nn.Linear(obs_dim, hid1_size)
        self.fc2 = nn.Linear(hid1_size, hid2_size)
        self.fc3 = nn.Linear(hid2_size, act_dim)

    def forward(self, obs):
        h1 = F.relu(self.fc1(obs))
        h2 = F.relu(self.fc2(h1))
        Q = self.fc3(h2)
        return Q
