#！/usr/bin/env python
#  -*- coding:utf-8 -*-
#  author:dabai time:2019/3/19

import  sys,argparse
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.spatial.distance import  squareform,pdist,cdist
from numpy.linalg import norm

width,height =640,480

class Boids:
    """Class that represents Boids simulation"""
    def __init__(self,N):
        """ 初始化模拟"""
        # 初始化位置 & 速度
        self.pos = [width / 2.0, height / 2.0] + 10 * np.random.rand(2 * N).reshape(N, 2)
        # 归一化随机速度
        angles = 2 * math.pi * np.random.rand(N)
        self.vel = np.array(list(zip(np.sin(angles), np.cos(angles))))
        self.N = N
        # min dist of approach
        self.minDist = 25.0
        # max magnitude of velocities calculated by "rules"
        self.maxRuleVel = 0.03
        # max magnitude of final velocity
        self.maxVel = 2.0

    def tick(self, frameNum, pts, beak):
        """在每个时间步更新模拟."""
        # get pairwise distances
        self.distMatrix = squareform(pdist(self.pos))
        # apply rules:
        self.vel += self.applyRules()
        self.limit(self.vel, self.maxVel)
        self.pos += self.vel
        self.applyBC()
        # update data
        pts.set_data(self.pos.reshape(2 * self.N)[::2],
                     self.pos.reshape(2 * self.N)[1::2])
        vec = self.pos + 10 * self.vel / self.maxVel
        beak.set_data(vec.reshape(2 * self.N)[::2],
                      vec.reshape(2 * self.N)[1::2])


    # 限制某些矢量的值，否则速度将在每个时间步无限制的增加，模拟将崩溃
    def limitVec(self, vec, maxVal):
        """limit magnitide of 2D vector"""
        mag = norm(vec)
        if mag > maxVal:
            vec[0], vec[1] = vec[0] * maxVal / mag, vec[1] * maxVal / mag

    # 定义limit()方法，限制数组中的值，采用模拟规则计算出的值
    def limit(self, X, maxVal):
        """limit magnitide of 2D vectors in array X to maxValue"""
        for vec in X:
            self.limitVec(vec, maxVal)


    # 设置边界条件
    def applyBC(self):
        """apply boundary conditions"""
        """四个if语句分别对应右侧，左侧，顶部，底部"""
        deltaR = 2.0
        for coord in self.pos:
            if coord[0] > width + deltaR:
                coord[0] = - deltaR
            if coord[0] < - deltaR:
                coord[0] = width + deltaR
            if coord[1] > height + deltaR:
                coord[1] = - deltaR
            if coord[1] < - deltaR:
                coord[1] = height + deltaR

    # 应用类鸟群规则
    def applyRules(self):
        # apply rule #1 - Separation：分离
        D = self.distMatrix < 25.0
        vel = self.pos * D.sum(axis=1).reshape(self.N, 1) - D.dot(self.pos)
        self.limit(vel, self.maxRuleVel)

        # different distance threshold
        D = self.distMatrix < 50.0

        # apply rule #2 - Alignment：列队
        vel2 = D.dot(self.vel)
        self.limit(vel2, self.maxRuleVel)
        vel += vel2

        # apply rule #1 - Cohesion：内聚
        vel3 = D.dot(self.pos) - self.pos
        self.limit(vel3, self.maxRuleVel)
        vel += vel3

        return vel

    # 添加个体
    def buttonPress(self, event):
        """event handler for matplotlib button presses"""
        # 点击鼠标左键，添加一个个体
        if event.button is 1:
            self.pos = np.concatenate((self.pos,
                                       np.array([[event.xdata, event.ydata]])),
                                      axis=0)
            # 随机速度矢量
            angles = 2 * math.pi * np.random.rand(1)
            v = np.array(list(zip(np.sin(angles), np.cos(angles))))
            self.vel = np.concatenate((self.vel, v), axis=0)
            self.N += 1
            # 点击鼠标右键，惊吓
        elif event.button is 3:
            # 在干扰出现的点的相反方向上增加一个速度分量
            self.vel += 0.1 * (self.pos - np.array([[event.xdata, event.ydata]]))



def tick(frameNum, pts, beak, boids):
    #print frameNum
    """update function for animation"""
    # boids.tick()在每个时间步被调用，以便更新动画
    boids.tick(frameNum, pts, beak)
    return pts, beak

# 主函数

def main():
  # use sys.argv if needed
  print('starting boids...')

  # 添加命令行选项
  parser = argparse.ArgumentParser(description="Implementing Craig Reynold's Boids...")
  # add arguments
  parser.add_argument('--num-boids', dest='N', required=False)
  args = parser.parse_args()

  # 添加各种命令行选项
  # number of boids
  N = 100
  if args.N:
      N = int(args.N)

  # create boids
  boids = Boids(N)

  # 绘制类鸟群个体的身体和头部
  fig = plt.figure()
  ax = plt.axes(xlim=(0, width), ylim=(0, height))

  pts, = ax.plot([], [], markersize=10,
                  c='k', marker='o', ls='None')
  beak, = ax.plot([], [], markersize=4,
                  c='r', marker='o', ls='None')
  anim = animation.FuncAnimation(fig, tick, fargs=(pts, beak, boids),
                                 interval=50)

  # 用 mpl_connect()方法向 matplotlib 画布添加一个按钮按下事件。
  # 每次在模拟窗口按下鼠标时，buttonPress()方法都会被调用。
  cid = fig.canvas.mpl_connect('button_press_event', boids.buttonPress)

  plt.show()

# 调用主函数
if __name__ == '__main__':
  main()