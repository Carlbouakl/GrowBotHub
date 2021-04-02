#!/usr/bin/env python3.7

import os
import rospy

def check_for_safety_error():
    return False
    # rospy.wait_for_service('Safety')
    # safety_srv = rospy.ServiceProxy('Safety', Safety)
    # try:
    #     return (safety_srv())
    # except Exception as e:
    #     return ('Software-Error: Safety Service not responding')


def wait_for_start():
    pass
    # rospy.wait_for_service('Start')
    # start_srv = rospy.ServiceProxy('Start', Start)
    # try:
    #     return (start_srv())
    # except Exception as e:
    #     return ('Software-Error: Start Service not responding')

def wait_for_solve(reason):
    pass
    # if (reason == 'safety'):
    #     print('Safety Error')
    # elif(reason == 'Hardware Defect'):
    #     print('Harware Error')
    # elif(reason == 'moving_service_error'):
    #     print('Movement Error')
    # else:
    #     print(reason, + 'Error')
    #
    # rospy.wait_for_service('Relaunch')
    # safety_srv = rospy.ServiceProxy('Relaunch', Safety)
