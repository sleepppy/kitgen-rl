from env import AwesEnv
from rl2 import DDPG
import numpy as np
import matplotlib.pyplot as plt
import os

MAX_EPISODES = 10
MAX_EP_STEPS = 2000
ON_TRAIN = True

path = "./plots/test/"
window_size = 30
rewards = []

# set env
env = AwesEnv()
s_dim = env.state_dim
a_dim = env.action_dim
a_bound = env.action_bound

# set RL method (continuous)
rl = DDPG(a_dim, s_dim, a_bound)


def train():
    # start training
    for i in range(MAX_EPISODES):
        s = env.reset()
        ep_r = 0.

        theta0 = []
        phi0 = []
        r0 = []

        for j in range(MAX_EP_STEPS):

            a = rl.choose_action(np.array(s))

            s_, r, done = env.step(a)

            rl.store_transition(s, a, r, s_)

            ep_r += r
            if rl.memory_full:
                # start to learn once has fulfilled the memory
                rl.learn()

            s = s_

            theta0.append(s[0])
            phi0.append(s[1])
            r0.append(s[2])

            if done or j == MAX_EP_STEPS - 1:
                print('Ep: %i | %s | ep_r: %.1f | steps: %i' % (i, '---' if not done else 'done', ep_r, j))
                rewards.append(ep_r)

                theta0 = np.array(theta0)
                phi0 = np.array(phi0)
                r0 = np.array(r0)

                x = np.multiply(r0, np.multiply(np.sin(theta0), np.cos(phi0)))
                y = np.multiply(r0, np.multiply(np.sin(theta0), np.sin(phi0)))
                z = np.multiply(r0, np.cos(theta0))
                line, = ax.plot(x, y, z, '-')
                ax.set_xlabel("x")
                ax.set_ylabel("y")
                ax.set_zlabel("z")
                break
    rl.save()


def eval():
    rl.restore()

    while True:
        s = env.reset()
        for _ in range(200):
            a = rl.choose_action(s)
            s, r, done = env.step(a)
            if done:
                break


if ON_TRAIN:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    train()
else:
    eval()

plt.savefig(path+"traj.png")
plt.show()

plt.figure()
plt.plot(rewards, '-')
plt.savefig(path+"rewards.png")
plt.show()
