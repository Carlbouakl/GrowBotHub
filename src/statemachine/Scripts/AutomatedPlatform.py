#!/usr/bin/env python3.7

class AutomatedPlatform:
    """
    Class representing a platform whose role is to move growth modules
    """
    def __init__(self, startPosition):
        self.position=startPosition # Location in x,y,z and yaw
        self.loaded = False # Carrying Growth module or not
        self.status = 'Standby' # Moving or Standby


    """CLASS METHODS/FUNCTIONS"""
    def move(self):
        pass


""" LISTENER """
if __name__ == "__main__":
    print('Error: ',AutomatedPlatform.__name__ ,' executed as main')
