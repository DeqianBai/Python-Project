#！/usr/bin/env python
#  -*- coding:utf-8 -*-
#  author:dabai time:2019/4/2

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

t = np.linspace(0, 10, 500)
x = np.cos(2 * np.pi * t)
y = np.sin(2 * np.pi * t)


ax1.set_ylabel(u'cos(2\u03c0t)')
ax1.set_xlim(0, 10)
ax1.set_ylim(-1, 1)
plt.setp(ax1.get_xticklabels(),visible=False)

ax2.set_xlabel('t')
ax2.set_ylabel(u'sin(2\u03c0t)')
ax2.set_xlim(0, 10)
ax2.set_ylim(-1, 1)

lines = []
for i in range(len(t)):
    head = i - 1
    head_slice = (t > t[i] - 1.0) & (t < t[i])
    line1,  = ax1.plot(t[:i], x[:i], color='black')
    line1a, = ax1.plot(t[head_slice], x[head_slice], color='red', linewidth=2)
    line1e, = ax1.plot(t[head], x[head], color='red', marker='o', markeredgecolor='r')
    line2,  = ax2.plot(t[:i], y[:i], color='black')
    line2a, = ax2.plot(t[head_slice], y[head_slice], color='red', linewidth=2)
    line2e, = ax2.plot(t[head], y[head], color='red', marker='o', markeredgecolor='r')
    lines.append([line1,line1a,line1e,line2,line2a,line2e])


# Build the animation using ArtistAnimation function

ani = animation.ArtistAnimation(fig,lines,interval=50,blit=True)
plt.show()

fn = 'combine_two_2d_animations_artistanimation'
ani.save('%s.mp4'%(fn),writer='ffmpeg')
#ani.save('%s.gif'%(fn),writer='imagemagick')