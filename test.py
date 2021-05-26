import numpy as np

class AwesEnv(object):
    action_bound = [-1, 1]  # TODO：动作范围
    goal = {'x': 100., 'y': 100., 'l': 40}  # 蓝色 goal 的 x,y 坐标和长度 l
    state_dim = 3  # 三个观测值：两个角度一个距离
    action_dim = 1  # rref



    def __init__(self):
        self.kite_info = np.zeros([5, 1], dtype=np.float32)  # 存储风筝信息
        # 生成出 (5,1) 的矩阵
        self.kite_info[0] = 200  # 风筝长度

    def step(self, action):
        done = False
        kitedis = self.kite_info[1]  # distance
        kiteang2 = self.kite_info[2]  # angle Θ 和z轴的角度
        kiteang3 = self.kite_info[3]  # angle 和XOY平面的角度

        kiteroll = self.kite_info[4]  # roll angle 倾角



        先把系统状态的得到，以及风速
        wind = compute_wind()

       #预测控制率得到倾角
        self.kite_info[4] = f(action)



        # state (之后会变)
        s = self.kite_info

        # 回合结束：r达到最长
        # 所以需要计算 finger 的坐标
        (a1l, a2l) = self.arm_info['l']  # radius, arm length
        (a1r, a2r) = self.arm_info['r']  # radian, angle
        a1xy = np.array([200., 200.])    # a1 start (x0, y0)
        a1xy_ = np.array([np.cos(a1r), np.sin(a1r)]) * a1l + a1xy  # a1 end and a2 start (x1, y1)
        finger = np.array([np.cos(a1r + a2r), np.sin(a1r + a2r)]) * a2l + a1xy_  # a2 end (x2, y2)

        # 根据 finger 和 goal 的坐标得出 done and reward
        if self.goal['x'] - self.goal['l']/2 < finger[0] < self.goal['x'] + self.goal['l']/2:
            if self.goal['y'] - self.goal['l']/2 < finger[1] < self.goal['y'] + self.goal['l']/2:
                done = True
                r = 1.      # finger 在 goal 以内
        return s, r, done

    def reset(self):
        pass



if __name__ == '__main__':
    env = AwesEnv()
    while True:
        env.render()
