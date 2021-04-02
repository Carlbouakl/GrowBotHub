#!/usr/bin/env python3.7
import os
import numpy as np

class AUTOMATEDPLATFORM:

    """INITIALIZATION"""
    def __init__(self):
        self.Pose # Location in x,y,z and yaw
        self.Loaded = False # Carrying Growth module or not
        self.Status = 'Standby' # Moving or Standby


    """CLASS METHODS/FUNCTIONS"""
    def move(self):
        pass


""" LISTENER """
if __name__ == "__main__":
    print('AUTOMATED_PLATFORM_CLASS')
