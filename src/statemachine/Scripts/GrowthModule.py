#!/usr/bin/env python3.7

class GrowthModule:
    """
    Represents a container where plants are placed to grow
    """
    """INITIALIZATION"""
    def __init__(self,id,plants,capacity,location,weight,dimensions):
        self.id = id
        self.plants=plants #List of stored plants
        self.capacity=capacity #Number of plants it can store
        self.location=location #location on the shelf or in the robotics station?
        self.weight=weight #kg
        self.dimensions=dimensions #(height,width)


    """CLASS METHODS/FUNCTIONS"""
    def move(self):
        pass


""" LISTENER """
if __name__ == "__main__":
   print('Error: ',GrowthModule.__name__ ,' executed as main')
