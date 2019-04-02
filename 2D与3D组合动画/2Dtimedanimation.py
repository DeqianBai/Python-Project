#！/usr/bin/env python
#  -*- coding:utf-8 -*-
#  author:dabai time:2019/4/2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation

# 定义FuncAnimation function调用的动画函数

class SubplotAnimation(animation.TimedAnimation):
    def __init__(self):
        fig = plt.figure()
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)

        self.t = np.linspace(0, 10, 500)
        self.x = np.cos(2 * np.pi * self.t)
        self.y = np.sin(2 * np.pi * self.t)

        ax1.set_ylabel(u'cos(2\u03c0t)')
        self.line1 = Line2D([], [], color='black')
        self.line1a = Line2D([], [], color='red', linewidth=2)
        self.line1e = Line2D(
            [], [], color='red', marker='o', markeredgecolor='r')
        ax1.add_line(self.line1)
        ax1.add_line(self.line1a)
        ax1.add_line(self.line1e)
        ax1.set_xlim(0, 10)
        ax1.set_ylim(-1, 1)
        plt.setp(ax1.get_xticklabels(),visible=False)

        ax2.set_xlabel('t')
        ax2.set_ylabel(u'sin(2\u03c0t)')
        self.line2 = Line2D([], [], color='black')
        self.line2a = Line2D([], [], color='red', linewidth=2)
        self.line2e = Line2D(
            [], [], color='red', marker='o', markeredgecolor='r')
        ax2.add_line(self.line2)
        ax2.add_line(self.line2a)
        ax2.add_line(self.line2e)
        ax2.set_xlim(0, 10)
        ax2.set_ylim(-1, 1)

        animation.TimedAnimation.__init__(self, fig, interval=50, blit=True)

    def _draw_frame(self, framedata):
        i = framedata
        head = i - 1
        head_slice = (self.t > self.t[i] - 1.0) & (self.t < self.t[i])

        self.line1.set_data(self.t[:i], self.x[:i])
        self.line1a.set_data(self.t[head_slice], self.x[head_slice])
        self.line1e.set_data(self.t[head], self.x[head])

        self.line2.set_data(self.t[:i], self.y[:i])
        self.line2a.set_data(self.t[head_slice], self.y[head_slice])
        self.line2e.set_data(self.t[head], self.y[head])

        self._drawn_artists = [self.line1, self.line1a, self.line1e,
                               self.line2, self.line2a, self.line2e]

    def new_frame_seq(self):
        return iter(range(self.t.size))

    def _init_draw(self):
        lines = [self.line1, self.line1a, self.line1e,
                 self.line2, self.line2a, self.line2e]
        for l in lines:
            l.set_data([], [])



ani = SubplotAnimation()
plt.show()

fn = 'combine_two_2d_animations_timedanimation'
ani.save('%s.mp4'%(fn),writer='ffmpeg')