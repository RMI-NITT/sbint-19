#!/usr/bin/env python
import rospy
from sbhw.msg import mov
import pygame
import sys
import math as m
import numpy as np
from geometry_msgs.msg import Pose, Twist
from std_msgs.msg import Int32
from std_msgs.msg import Float64
import random as rnd
import geometry as g
import time

flag = 1
bpose =  Pose()
btwist = Twist()
ball = g.point(x = 0, y = 0)
ballv = g.point(x = 0,y = 0)
robot = g.point(x = 100,y= 100)

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

def talker():
    global robot
    global ball
    global ballv
    rospy.init_node('joystick', anonymous=True)
    pubd2 = rospy.Publisher('bot2d', Int32, queue_size = 10)
    pubk2 = rospy.Publisher('bot2k', Int32, queue_size = 10)
    pubv2 = rospy.Publisher('bot2mov',mov,queue_size = 10)
    rospy.Subscriber('ballpose', Pose, bcallback)
    rospy.Subscriber('bot2pose', Pose, botcallback)    
    rospy.Subscriber('balltwist', Twist, btcallback)
    rate = rospy.Rate(60)
    while not rospy.is_shutdown():
    	pygame.init()
    	rate = rospy.Rate(60)
    	pygame.joystick.init()
    	while True:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                	done=True 
            updatebpose(bpose,ball)
            updatebtwist(btwist,ballv)
            joystick_count = pygame.joystick.get_count()
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                name = joystick.get_name()
                axes = joystick.get_numaxes()
                vx = joystick.get_axis(3)
                vx = vx*abs(vx)
                vy = joystick.get_axis(4)
                vy = vy*abs(vy)
                ds = joystick.get_axis(5)
                hats = joystick.get_numhats()
                for i in range( hats ):
                	hat = joystick.get_hat( i )
                a,b = hat
                print a,b
                buttons = joystick.get_numbuttons()
                k = joystick.get_button(0) ## 0 or 1 -> kick
                s = joystick.get_button(1) # Switch robot
                LB = joystick.get_button(4) ## 0 or 1 -> anti-clockwise rotation
                RB = joystick.get_button(5) ## 0 or 1 -> clockwise rotation
            if(LB == 0 and RB ==1):
                wz = -0.1
            if(LB == 1 and RB ==0):
                wz = 0.1
            if( ( LB ==0 and RB == 0 ) or ( LB==1 and RB == 1 ) ):
                wz = 0
            vx = vx*0.06 
            vy = -vy*0.06 
            print 'vx',vx
            print 'vy',vy
            if ds < 0:
                ds = 0 ## value from 0 to 1
            ds = int(ds*255)
            tw = mov()
            tw.mode = 2
            tw.mag = vx**2 +vy**2
            if not(vx == 0) and vx > 0: 
                tw.thetav = m.atan(vy/vx)
            if not(vx == 0) and vx < 0 and vy < 0: 
                tw.thetav = m.atan(vy/vx) +-m.pi
            if not(vx == 0) and vx < 0 and vy > 0: 
                tw.thetav = m.atan(vy/vx) + m.pi
            tw.thetap = g.angb(robot,ball)
            print tw.mag,tw.thetav,tw.thetap
            pubv2.publish(tw)
            pubd2.publish(ds)
            pubk2.publish(k)
            rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass