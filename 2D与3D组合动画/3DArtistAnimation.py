#！/usr/bin/env python
#  -*- coding:utf-8 -*-
#  author:dabai time:2019/4/2

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3
from IPython.display import HTML

fig = plt.figure()
ax1 = fig.add_subplot(1, 2, 1, projection="3d")
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 4)

t = np.linspace(0, 80, 300)
x = np.cos(2 * np.pi * t / 10.)
y = np.sin(2 * np.pi * t / 10.)
z = 10 * t

ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_zlabel('z')
ax1.set_xlim(-1, 1)
ax1.set_ylim(-1, 1)
ax1.set_zlim(0, 800)

ax2.set_xlabel('y')
ax2.set_ylabel('z')
ax2.set_xlim(-1, 1)
ax2.set_ylim(0, 800)

ax3.set_xlabel('x')
ax3.set_ylabel('z')
ax3.set_xlim(-1, 1)
ax3.set_ylim(0, 800)

lines = []
for i in range(len(t)):
    head = i - 1
    head_slice = (t > t[i] - 1.0) & (t < t[i])
    # print(x[head],y[head],z[head])
    line1, = ax1.plot(x[:i], y[:i], z[:i],
                      color='black')
    line1a, = ax1.plot(x[head_slice], y[head_slice], z[head_slice],
                       color='red', linewidth=2)
    line1e, = ax1.plot([x[head]], [y[head]], [z[head]],
                       color='red', marker='o', markeredgecolor='r')
    line2, = ax2.plot(y[:i], z[:i],
                      color='black')
    line2a, = ax2.plot(y[head_slice], z[head_slice],
                       color='red', linewidth=2)
    line2e, = ax2.plot(y[head], z[head],
                       color='red', marker='o', markeredgecolor='r')
    line3, = ax3.plot(x[:i], z[:i],
                      color='black')
    line3a, = ax3.plot(x[head_slice], z[head_slice],
                       color='red', linewidth=2)
    line3e, = ax3.plot(x[head], z[head],
                       color='red', marker='o', markeredgecolor='r')
    lines.append([line1, line1a, line1e, line2, line2a, line2e, line3, line3a, line3e])

plt.tight_layout()

ani = animation.ArtistAnimation(fig, lines, interval=50, blit=True)

plt.show()

fn = 'line_animation_3d_with_two_2d_artistanimation'
ani.save('%s.mp4'%(fn), writer='ffmpeg',fps=1000/50)