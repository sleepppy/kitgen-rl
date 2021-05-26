import numpy as np
import pykite as pk


class AwesEnv(object):
    action_bound = [-1, 1]  # TODO:rref速度范围

    state_dim = 6  # 位置向量3 速度向量3
    action_dim = 1  # rref速度是动作 rref→roll angle

    def __init__(self):
        self.kite = pk.kite()

    def step(self, action):
        done = False
        action = np.clip(action, *self.action_bound)
        self.kite.simulate(step, wind)  # 湍流风和x轴风速
        # 奖励怎么算？两阶段能量评估不一样 算整个回合还是分阶段讨论

        # 回到原点时done
        if ():
            done = True
        r = self.kite.reward()
        return s, r, done

    def reset(self):
        self.kite.__init__(pk.vect(0, 0, 0), pk.vect(0, 0, 0))
        return self.kite

    def sample_action(self):
        return np.random.rand(2) - 0.5  # two radians


if __name__ == '__main__':
    env = AwesEnv()
    while True:
        env.step(env.sample_action())
