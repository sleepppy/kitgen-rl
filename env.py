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

        z = np.multiply(self.kite.position.r, np.cos(self.kite.position.theta))
        start_z = np.multiply(self.start_r, np.cos(self.start_theta))

        # self.kite.position.r > self.start_r and

        if s[2] < 30:
            r = r * (z - start_z)

        if s[2] == 30:
            arr = [self.kite.position.theta - self.start_theta, self.kite.position.phi - self.start_phi,
                   self.kite.position.r - self.start_r]
            r = (normalization(s[0], arr) + normalization(s[1], arr) + normalization(s[2], arr)) * r

        # 回到原点时done
        if self.kite.position.theta == self.start_theta and self.kite.position.phi == self.start_phi and self.kite.position.r == self.start_r:
            done = True
        else:
            if done == True:
                r = -r * 1000

        return s, r, done

    def reset(self):
        self.start_theta = np.pi / 6 * random.random()
        self.start_phi = 0.0
        self.start_r = 10.0 * random.random()
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
