#!/usr/bin/env python3.7

class RoboticStation:
    """Represents a robotic arm that can move plants 
    from one growth module to another"""
    
    """INITIALIZATION"""
    def __init__(self,capacity=2):
        self.capacity = capacity
        self.growthModuleCount = 0
        self.status = 'Free' # Free or Busy
        self.countdown = 0 # Time remaining until a job is finished


    """CLASS METHODS/FUNCTIONS"""
    def harvest(self):
        pass


""" LISTENER """
if __name__ == "__main__":
    print('Error: ',RoboticArm.__name__ ,' executed as main')
