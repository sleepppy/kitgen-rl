from env import AwesEnv
from rl import DDPG
import numpy as np
import matplotlib.pyplot as plt
import os

MAX_EPISODES = 500
MAX_EP_STEPS = 200
ON_TRAIN = True

path = "./plots/test/"
window_size = 30
rewards = []
theta0 = []
phi0 = []
r0 = []

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
        for j in range(MAX_EP_STEPS):

            a = rl.choose_action(s)

            s_, r, done = env.step(a)

            rl.store_transition(s, a, r, s_)

            ep_r += r
            if rl.memory_full:
                # start to learn once has fulfilled the memory
                rl.learn()

            s = s_

            theta0.append(s[0])
            phi0.append(s[1])
            r0.append(s[3])

            if done or j == MAX_EP_STEPS - 1:
                print('Ep: %i | %s | ep_r: %.1f | steps: %i' % (i, '---' if not done else 'done', ep_r, j))
                rewards.append(ep_r)
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
    train()
else:
    eval()

# try:
#     os.mkdir(path)
# except OSError:
#     pass
#
# def plot_trajectory(theta, phi, r, save=None, marker='-'):
#     fig=plt.figure()
#     ax = fig.add_subplot(111, projection = '3d')
#     x=np.multiply(r, np.multiply(np.sin(theta), np.cos(phi)))
#     y=np.multiply(r, np.multiply(np.sin(theta), np.sin(phi)))
#     z=np.multiply(r, np.cos(theta))
#     line,=ax.plot(x, y, z, marker)
#     ax.set_xlabel("x")
#     ax.set_ylabel("y")
#     ax.set_zlabel("z")
#     if save is not None:
#         plt.savefig(save)
#     plt.show()
#
# theta0=np.array(theta0)
# phi0=np.array(phi0)
# r0=np.array(r0)
#
# plot_trajectory(theta0, phi0, r0, save=path+"traj.png")
#
#
# plt.figure()
# plt.plot(rewards, 'o')
# plt.plot(np.convolve(rewards, np.ones(window_size), 'valid') / window_size)
# plt.savefig(path+"rewards.png")
# plt.show()
