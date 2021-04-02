#!/usr/bin/env python3.7
import os
import numpy as np

class SHELF:

    """INITIALIZATION"""
    def __init__(self):
        self.Capacity = rospy.get_param('SHELF_CAPACITY')
        self.Occupancy = rospy.get_param('SHELF_OCCUPANCY')
        self.Dimension = rospy.get_param('SHELF_DIMENSIONS')


    """CLASS METHODS/FUNCTIONS"""
    def unload(self):
        pass


""" LISTENER """
if __name__ == "__main__":
    print('SHELF_CLASS')
