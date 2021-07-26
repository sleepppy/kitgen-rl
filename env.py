import random

import numpy as np
import pykite as pk
import sys


def normalization(x, arr):
    return float(x - np.min(arr)) / (np.max(arr) - np.min(arr)) * 10


class AwesEnv(object):
    action_bound = [-4.0, 4.0]  # psi范围

    state_dim = 6  # 位置向量3 速度向量3
    action_dim = 1  # rref速度是动作 rref→roll angle 目前是

    start_theta = 0.0
    start_phi = 0.0
    start_r = 0.0

    def __init__(self):
        self.kite = pk.kite(pk.vect(0, 0.0, 0.0), pk.vect(0.0, 0.0, 0.0))

    def step(self, action):
        done = False
        action = np.clip(action, *self.action_bound)
        done = not self.kite.simulate(action)
        s = [self.kite.position.theta, self.kite.position.phi, self.kite.position.r,
             self.kite.velocity.theta, self.kite.velocity.phi, self.kite.velocity.r]

        r = self.kite.reward(action)

        # 回到原点时done
        if s[2] == 290:
            arr = [s[0], s[1]]
            r = -((1 - normalization(arr[0], arr)) + normalization(arr[1], arr)) * r

            if s[5] == 0:
                done = True
                print("arrive")
        else:
            if done == True:
                r = -10000

        return s, r, done

    def reset(self):
        self.start_theta = np.deg2rad(40)
        self.start_phi = np.deg2rad(5) * random.random()
        self.start_r = 105.0 * random.random()
        self.kite = pk.kite(pk.vect(self.start_theta, self.start_phi, self.start_r), pk.vect(0.0, 0.0, 0.0))

        s = [self.kite.position.theta, self.kite.position.phi, self.kite.position.r,
             self.kite.velocity.theta, self.kite.velocity.phi, self.kite.velocity.r]
        return s

    def sample_action(self):
        return np.rad2deg(-0.05)  # two radians


if __name__ == '__main__':
    env = AwesEnv()
    while True:
        env.step(env.sample_action())
