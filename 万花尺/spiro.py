#！/usr/bin/env python
#  -*- coding:utf-8 -*-
#  author:dabai time:2019/3/13


import sys, random, argparse
import numpy as np
import math
import turtle
import random
from PIL import Image
from datetime import datetime
from fractions import gcd

# a class that draws a spirograph
class Spiro:

    # constructor
    def __init__(self,xc,yc,col,R,r,l):

        self.t=turtle.Turtle()
        # set the cursor shape
        self.t.shape('turtle')
        # set the step in degrees
        self.step=5
        # set the drawing complete flag
        self.drawingComplete=False

        # set the paprameters
        self.setparams(xc,yc,col,R,r,l)

        # initialize the drawing
        self.restart()

    def setparams(self, xc, yc, col, R, r, l):
        # the Spirograph parameters
        self.xc=xc
        self.yc=yc
        self.R=int(R)
        self.r=int(r)
        self.l=l
        self.col=col
        # reduce r/R to its smallest from by dividing with the GCD
        gcdVal=gcd(self.r,self.R)
        self.nRot=self.r//gcdVal
        # get ratio of radii
        self.k=r/float(R)
        # set the color
        self.t.color(*col)
        # store the current angle
        self.a=0


    # restart the drawing
    def restart(self):
        # set the flag
        self.drawingComplete=False
        # show the turtle
        self.t.showturtle()
        # go to the first point
        self.t.up() # 提笔
        R,k,l=self.R,self.k,self.l
        a=0.0
        x=R*((1-k)*math.cos(a)+l*math.cos((1-k)*a/k))
        y=R*((1-k)*math.sin(a)-l*math.sin((1-k)*a/k))

        self.t.setpos(self.xc+x,self.yc+y)
        self.t.down() # 落笔



    # draw the whole thing
    def draw(self):
        # draw the reset of the points
        R, k, l = self.R, self.k, self.l
        for i in range(0,360*self.nRot+1,self.step):
            a=math.radians(i)
            x = R * ((1 - k) * math.cos(a) + l * math.cos((1 - k) * a / k))
            y = R * ((1 - k) * math.sin(a) - l * math.sin((1 - k) * a / k))
            self.t.setpos(self.xc+x,self.yc+y)
            # drawing is now done so hide the turtle cursor
            self.t.hideturtle()


    # update by one step
    def update(self):

        # skip the rest of the steps if done
        if self.drawingComplete:
            return
        # increment the angle
        self.a+=self.step
        R,k,l=self.R, self.k, self.l
        # set the angle
        a=math.radians(self.a)
        x=self.R*((1 - k) * math.cos(a) + l * math.cos((1 - k) * a / k))
        y = R * ((1 - k) * math.sin(a) - l * math.sin((1 - k) * a / k))
        self.t.setpos(self.xc+x, self.yc+y)
        # if drawing is complete,set the flag
        if self.a>=360*self.nRot:
            self.drawingComplete=True
            # drawing is now done so hide the turtle cursor
            self.t.hideturtle()


    # clear everything
    def clear(self):
        self.t.clear()

# A class for animating spirographs
class SpiroAnimator:
    # constructor
    def __init__(self,N):
        # timer value in milliseconds
        self.deltaT=10
        # get window dimensions
        self.width = turtle.window_width()
        self.height=turtle.window_height()
        # creat the Spiro objects
        self.spiros=[]
        for i in range(N):
            # generate random params
            rparams=self.genRandomParams()
            # set spiro params
            spiro=Spiro(*rparams)
            self.spiros.append(spiro)
        # call timer
        turtle.ontimer(self.update,self.deltaT)



    # restart spiro drawing
    def restart(self):
        for spiro in self.spiros:
            # clear
            spiro.clear()
            # generate random parameters
            rparams=self.genRandomParams()
            # set spiro params(*rparams)
            spiro.setparams(*rparams)
            # restart drawing
            spiro.restart()


    # generate random parameters
    def genRandomParams(self):
        width,height=self.width,self.height
        R=random.randint(50,min(width,height)//2)
        r=random.randint(10,9*R//10)
        l = random.uniform(0.1, 0.9)
        xc = random.randint(-width // 2, width // 2)
        yc = random.randint(-height // 2, height // 2)
        col=(random.random(),
             random.random(),
             random.random())
        return (xc,yc,col,R,r,l)

    def update(self):
        # update all spiros
        nComplete=0
        for spiro in self.spiros:
            # update
            spiro.update()
            # count completed ones
            if spiro.drawingComplete:
                nComplete+=1
        # if all spiros are complete,restart
        if nComplete==len(self.spiros):
            self.restart()
        # call timer
        turtle.ontimer(self.update,self.deltaT)

    # toggle turtle on/off
    def toggleTurtles(self):
        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()

            else:
                spiro.t.showturtle()


def saveDrawing():
    # hide the turtle cursor
    turtle.hideturtle()
    # generate unique file name
    dateStr = (datetime.now()).strftime("%d%b%Y-%H%M%S")
    fileName = 'spiro-' + dateStr
    print('saving drawing to %s.eps/png' % fileName)
    # get tkinter canvas
    canvas = turtle.getcanvas()
    # save postscript image
    canvas.postscript(file=fileName + '.eps')
    # use PIL to convert to PNG
    img = Image.open(fileName + '.eps')
    img.save(fileName + '.png', 'png')
    # show turtle
    turtle.showturtle()


# main()function

def main():
    # use sys.argv if needed
    print('genterating spirograph...')
    # create parser
    descStr ="""This program draws spirographs using the Turtle module. 
    When run with no arguments, this program draws random spirographs.
    
    Terminology:
    R: radius of outer circle.
    r: radius of inner circle.
    l: ratio of hole distance to r."""
    parser = argparse.ArgumentParser(description=descStr) # 创建参数解析器对象

    parser.add_argument('--sparams',nargs=3,dest='sparams',required=False,
                        help="The three arguments in sparams:R,r,l.") # 向解析器添加可选参数

    # parse args
    args=parser.parse_args() # 调用函数进行实际的解析

    # set to 80% screen width
    turtle.setup(width=0.8)

    # set cursor shape
    turtle.shape('turtle')

    # set title
    turtle.title("Spirographs!")
    # add key handler for saving image
    turtle.onkey(saveDrawing,"s")
    # start listening
    turtle.listen()

    # hide main turtle cursor
    turtle.hideturtle()

    # checks args and draw # 首先检查是否有参数赋给--sparams.如果有，就从字符串中提取他们，用“列表解析”将他们转换成浮点数
    if args.sparams:
        params=[float(x) for x in args.sparams]
        # draw spirograph with given parameters
        # black by default
        col=(0.0,0.0,0.0)
        spiro=Spiro(0,0,col,*params)
        spiro.draw()

    else:
        # creat animator object
        spiroAnim=SpiroAnimator(4)
        # add key handler to toggle turtle cursor
        turtle.onkey(spiroAnim.toggleTurtles,"t")
        # add key handler to toggle turtle cursor
        turtle.onkey(spiroAnim.restart,"space")

    # start turtle main loop

        turtle.mainloop()


# call main
if __name__ == '__main__':
    main()















