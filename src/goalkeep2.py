#!/usr/bin/env python
import sys
import rospy
import math as m
import numpy as np
from geometry_msgs.msg import Pose, Twist
from std_msgs.msg import Int32
from std_msgs.msg import Float64
import random as rnd
from sbhw.msg import mov
import geometry as g
import time

flag = 1
bpose =  Pose()
btwist = Twist()
ball = g.point(x = 0, y = 0)
ballv = g.point(x = 0,y = 0)
robot = g.point(x = 0,y= 0)

def bcallback(msg):
    global bpose
    bpose = msg

def btcallback(msg):
    global btwist
    btwist = msg

def updatebtwist(a,b):
    b.x = a.linear.x
    b.y = a.linear.y

def updatebpose(a,b):
    b.x = a.position.x
    b.y = a.position.y

def botcallback(msg):
    global robot
    global ball
    robot.x = msg.position.x
    robot.y = msg.position.y

def summa():
    global robot
    global ball
    global ballv
    global d
    global gs
    rospy.init_node('autogk',anonymous=True)
    r1 = rospy.Publisher('bot1mov',mov, queue_size = 10)
    rospy.Subscriber('ballpose', Pose, bcallback)
    rospy.Subscriber('bot1pose', Pose, botcallback)    
    rospy.Subscriber('balltwist', Twist, btcallback)
    updatebpose(bpose,ball)
    updatebtwist(btwist,ballv)
    r = mov()
    rate = rospy.Rate(10)
    while(True):
        r.x = 0
        r.y  = 0  
        r.mode = 1
        r1.publish(r)
        rate.sleep()
        while(True):
            updatebpose(bpose,ball)
            updatebtwist(btwist,ballv)
            if not(ballv.x == 0):
                m0 = ballv.y/ballv.x
                th = m.atan(m0)
                th = 3.14 + th
                q = m.tan(th/2)
                k = 210
                xb= ball.x
                yb= ball.y
                xtg = k
                ytg = m0*(k-xb)+yb
                if abs(ytg)>=150:
                    ytg = 0
                r.x = xtg
                r.y = ytg  
                r.mode = 1
                r.thetap = m.pi
                r1.publish(r)
            else:  
                r.x = -210
                r.y = 0
                r.mode = 1
                r.thetap = m.pi
                r1.publish(r)

            rate.sleep()
            

if __name__ == '__main__':
    summa()
    