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
            r.x = ball.x
            r.y = ball.y
            r.thetap = g.angb(ball,robot)
            r1.publish(r)
            rate.sleep()
            

if __name__ == '__main__':
    summa()