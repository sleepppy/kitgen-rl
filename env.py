import numpy as np
import pykite as pk
import sys


class AwesEnv(object):
    action_bound = [-4, 4]  # psi范围

    state_dim = 6  # 位置向量3 速度向量3
    action_dim = 1  # rref速度是动作 rref→roll angle 目前是

    def __init__(self):
        self.kite = pk.kite(pk.vect(np.pi / 6, 0.0, 50.0), pk.vect(0.0, 0.0, 0.0))

    def step(self, action):
        done = False
        action = np.clip(action, *self.action_bound)
        done = not self.kite.simulate(self, action)
        s = [self.kite.position.theta, self.kite.position.phi, self.kite.position.r,
             self.kite.velocity.theta, self.kite.velocity.phi, self.kite.velocity.r]

        r = self.kite.reward()

        # 回到原点时done
        if self.kite.position.theta == 0 and self.kite.position.phi == 0 and self.kite.position.r == 0:
            done = True
        else:
            if done == True:
                r = -sys.maxsize - 1

        return s, r, done

    def reset(self):
        s = [self.kite.position.theta, self.kite.position.phi, self.kite.position.r,
             self.kite.velocity.theta, self.kite.velocity.phi, self.kite.velocity.r]
        return s

    def sample_action(self):
        return -0.05  # two radians


if __name__ == '__main__':
    env = AwesEnv()
    while True:
        env.step(env.sample_action())
