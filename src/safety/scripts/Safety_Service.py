#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import rospy
import time
import Safety # Python script
home_directory = os.getenv("HOME")


def handle_safety(request):
    """Safety Callback function - returns scan of safety"""
    rospy.loginfo(rospy.get_caller_id() + " safety")
    safety_scan = safetyResponse()
    safety_scan = Safety.safety()
    return safety_scan


def safety_server():
    """This function initiates the safety service."""
    rospy.init_node('safety_detection_server')
    service = rospy.Service('Safety_Detection', SafetySRV, Safety)
    rospy.loginfo('Starting Service Safety_Scan.')
    rospy.spin()

if __name__ == "__main__":
    safety_server()
