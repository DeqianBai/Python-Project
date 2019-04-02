#！/usr/bin/env python
#  -*- coding:utf-8 -*-
#  author:dabai time:2019/4/2

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d.art3d import Line3D

# 定义在FuncAnimation function中使用的动画方程
class SubplotAnimation(animation.TimedAnimation):
    def __init__(self):
        fig=plt.figure()
        ax1=fig.add_subplot(1,2,1,projection="3d")
        ax2=fig.add_subplot(2,2,2,)
        ax3=fig.add_subplot(2,2,2)

        self.t=np.linspace(0,80,300)
        self.x=np.cos(2*np.pi*self.t/10)
        self.y=np.sin(2*np.pi*self.t/10)
        self.z=10*self.t


        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.set_zlabel('z')
        self.line1=Line3D([],[],[],color='black')
        self.line1a=Line3D([],[],[],color='red',linewidth=2)
        self.line1e=Line3D([],[],[],color='red',marker='o',markeredgecolor='r')
        ax1.add_line(self.line1)
        ax1.add_line(self.line1a)
        ax1.add_line(self.line1e)
        ax1.set_xlim(-1,1)
        ax1.set_ylim(-1,1)
        ax1.set_zlim(0,800)

        ax2.set_xlabel('y')
        ax2.set_ylabel('z')
        self.line2=Line2D([],[],color='black')
        self.line2a=Line2D([],[],color='red',linewidth=2)
        self.line2e=Line2D([],[],color='red',marker='o',markeredgecolor='r')
        ax2.add_line(self.line2)
        ax2.add_line(self.line2a)
        ax2.add_line(self.line2e)
        ax2.set_xlim(-1,1)
        ax2.set_ylim(0,800)

        ax3.set_xlabel('x')
        ax3.set_ylabel('z')
        self.line3 = Line2D([], [], color='black')
        self.line3a = Line2D([], [], color='red', linewidth=2)
        self.line3e = Line2D([],[],color='red',marker='o',markeredgecolor='r')
        ax3.add_line(self.line3)
        ax3.add_line(self.line3a)
        ax3.add_line(self.line3e)
        ax3.set_xlim(-1,1)
        ax3.set_ylim(0,800)
        plt.tight_layout()
        animation.TimedAnimation.__init__(self,fig,interval=50,blit=True)


    def _draw_frame(self, framedata):
        i=framedata
        head=i-1
        head_slice=(self.t>self.t[i]-1.0)&(self.t<self.t[i])

        self.line1.set_data(self.x[:i],self.y[:i])
        self.line1.set_3d_properties(self.z[:i])
        self.line1a.set_data(self.x[head_slice],self.y[head_slice])
        self.line1a.set_3d_properties(self.z[head_slice])
        self.line1e.set_data(self.x[head],self.y[head])
        self.line1e.set_3d_properties(self.z[head])

        self.line2.set_data(self.y[:i],self.z[:i])
        self.line2a.set_data(self.y[head_slice], self.z[head_slice])
        self.line2e.set_data(self.y[head], self.z[head])

        self.line3.set_data(self.x[:i], self.z[:i])
        self.line3a.set_data(self.x[head_slice], self.z[head_slice])
        self.line3e.set_data(self.x[head], self.z[head])

        self._drawn_artists = [self.line1, self.line1a, self.line1e,
                               self.line2, self.line2a, self.line2e,
                               self.line3, self.line3a, self.line3e]


    def new_frame_seq(self):
        return iter(range(self.t.size))

    def _init_draw(self):
        lines=[self.line1,self.line1a,self.line1e,
               self.line2,self.line2a,self.line2e,
               self.line3,self.line3a,self.line3e]

        for I in lines:
            I.set_data([],[])


ani=SubplotAnimation()

plt.show()
fn = 'line_animation_3d_with_two_2d_timedanimation'
ani.save('%s.mp4'%(fn), writer='ffmpeg',fps=1000/50)