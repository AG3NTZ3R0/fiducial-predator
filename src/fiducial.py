#!/usr/bin/env python

'''
A module for a robot class specialized to identify fiducials.
'''

import rospy

from geometry_msgs.msg import Twist
from fiducial_msgs.msg import FiducialTransformArray


class Fiducial:
    '''A robot that specializes in the identification and location of fiducials.'''
    def __init__(self):
        '''Initialize necessary publishers, subscribers, and messages.'''
        # Publisher
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

        # Subscriber
        self.fid_tf_sub = rospy.Subscriber('fiducial_transforms', FiducialTransformArray, self.fid_tf_cb)

        # Instance Variables
        # cmd_vel
        self.twist = Twist()

        # fiducial_transforms
        self.got_fid = False

    def fid_tf_cb(self, msg):
        '''The callback to capture and process the fiducial transform topic published by the aruco_detect package.'''
        try:
            fid = msg.transforms[0]
            
            self.got_fid = True
        except IndexError:
            self.got_fid = False

    def attack(self):
        '''Attack prey.'''
        rate = rospy.Rate(2.5)

        while not rospy.is_shutdown():
            if self.got_fid:
                self.twist.linear.x = 0.5
                self.twist.angular.z = 0
            else:
                self.twist.linear.x = 0
                self.twist.angular.z = 0.25

            self.cmd_vel_pub.publish(self.twist)
            rate.sleep()


if __name__ == '__main__':
    rospy.init_node("fiducial_project")
    robot = Fiducial()
    robot.attack()
