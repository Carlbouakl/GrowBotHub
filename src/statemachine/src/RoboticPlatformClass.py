#!/usr/bin/env python3.7
import os
import numpy as np

class ROBOTICARM:

    """INITIALIZATION"""
    def __init__(self):
        self.NbrGrowthModules = 0
        self.Status = 'Free' # Free or busy
        self.Countdown = 0 # Time it needs to finish job


    """CLASS METHODS/FUNCTIONS"""
    def harvest(self):
        pass


""" LISTENER """
if __name__ == "__main__":
    print('KUKA_CLASS')
