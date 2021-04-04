#!/usr/bin/env python3.7

class Shelf:
    """
    Represents a shelf where growth modules are stored 
    """

#REMARK:  the rospy data should be passed as a parameter to the function, the code
# should not be aware about rospy
 #rospy.get_param('SHELF_CAPACITY')
 #rospy.get_param('SHELF_OCCUPANCY')
 #rospy.get_param('SHELF_DIMENSIONS')
    """INITIALIZATION"""
    def __init__(self,capacity,occupancy,dimension):
        self.capacity = capacity # number of growthModules it can contain
        self.occupancy = occupancy #2D array of growthModules
        self.dimension = dimension #(height,width) in centimeters?


    """CLASS METHODS/FUNCTIONS"""
    def unload(self):
        pass


""" LISTENER """
if __name__ == "__main__":
     print('Error: ',Shelf.__name__ ,' executed as main')
