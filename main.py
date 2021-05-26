from env import AwesEnv
from rl import DDPG

MAX_EPISODES = 500
MAX_EP_STEPS = 200
ON_TRAIN = True

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
            if done or j == MAX_EP_STEPS - 1:
                print('Ep: %i | %s | ep_r: %.1f | steps: %i' % (i, '---' if not done else 'done', ep_r, j))
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
