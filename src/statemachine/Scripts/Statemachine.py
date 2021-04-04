#!/usr/bin/env python3.8

import os
import numpy as np
import rospy
import smach
import smach_ros
import logic
from Shelf import Shelf as shelf
from AutomatedPlatform import AutomatedPlatform as AP
from GrowthModule import GrowthModule as growth_module
from RoboticStation import RoboticStation as RS # Robotic Station

## TODO: create check_for_safety_error service on ROS
## TODO: create a move function
## TODO: Add state for switching growth module from one location to another

home_position = rospy.get_param('HOMEPOSITION')

class Initialization(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['start_homing'], input_keys=[], output_keys=[])

    def execute(self,userdata):
        userdata.test = rospy.get_param('TARE_WEIGHT') # Load parameters and classes here

        # handle safety errors that are present on startup
        if check_for_safety_error():
            wait_for_solve(reason='safety')

        return 'start_homing'


class Homing(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success','error'], input_keys=[], output_keys=[])

    def execute(self, userdata):
        # moving_result = move(home_position)
        print("Moving")
        if check_for_safety_error():
            wait_for_solve(reason = 'safety')
            return 'error'

        # elif moving_result == 'Paused':
        #     wait_for_solve(reason='pause')
        #     return 'error'

        # elif moving_result != 'The position is reached':
        #     wait_for_solve(reason= 'moving_service_error')
        #     return 'error'
        else:
            wait_for_start()
            AP.position = home_position
            return 'success' # TODO: Rename this accroding to what the name of the next state is


class GoToGrowthModule(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['success','error'], input_keys=[], output_keys=[])

    def execute(self, userdata): # userdata has the growth_module.ID and the location you want to go to
        #REMARK: occupancy could be an array of growthModule=> set to None if no growthModule
        if shelf.occupancy(userdata.ID) == False:
            print('Growth Module in this location does not exist')
            return 'error'
        elif AP.status == 'Busy':
            print('Automated platform is already doing a job')
            return 'error'
        elif userdata.position > shelf.dimension:
            print('Growth module outside the shelf')
            return 'error'
        else:
            moving_result = move(growth_module.location(userdata)) ## TODO: Put the coordinates of the growth Module
            if check_for_safety_error():
                wait_for_solve(reason = 'safety')
                return 'error'
            else:
                AP.position = growth_module.location(userdata)
                return'sucess'


class PickFromShelf(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['success','error'], input_keys=[], output_keys=[])

    def execute(self, userdata): # userdata has the growth_module.ID
        if shelf.occupancy(userdata) == False:
            print('Growth Module in this location does not exist')
            return 'error'
        elif AP.position != userdata: # i.e, the automated platform is not in the proper location
            print('Automated platform is not in the correct position')
            return 'error'
        if AP.loaded == True:
            print('Automated Platform is already carrying a Growth Module')
            return 'error'
        else:
            moving_result = pick()
            if check_for_safety_error():
                wait_for_solve(reason = 'safety')
                return 'error'
            else:
                AP.loaded = True
                AP.status = 'Moving'
                shelf.occupancy = 0 # TODO: Fix this to decide which growth module is 0 or 1 (and fix below)
                return 'go_to_robotic_station'

class GoToRoboticStation(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['success','error'], input_keys=[], output_keys=[])

    def execute(self, userdata): # userdata has the growth_module.ID
        if AP.loaded == False:
            print('Automated Platform is not carrying a Growth Module')
            return 'error'
        elif AP.pose != userdata: # i.e, the automated platform is not in the proper location ## TODO: Check for positon, not userdata
            print('Automated platform is not in the correct position')
            return 'error'
        elif RS.status == 'Busy':
            print('Robotic Station does not have space for an additional growth module')
            return 'error'
        else:
            moving_result = pick()
            if check_for_safety_error():
                wait_for_solve(reason = 'safety')
                return 'error'
            else:
                AP.position = RS_position ## TODO: ROS params define a location for this
                return 'deposit_roboti_station'

class DepositRoboticStation(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['success','error'], input_keys=[], output_keys=[])

    def execute(self, userdata): # userdata has the growth_module.ID
        if RS.status == 'Busy':
            print('Robotic Station does not have space for an additional growth module')
            return 'error'
        elif AP.position != RS_position: # i.e, the automated platform is not in the proper location
            print('Automated platform is not in the correct position')
            return 'error'
        else:
            moving_result = deposit()
            if check_for_safety_error():
                wait_for_solve(reason = 'safety')
                return 'error'
            else:
                AP.position = RS_position ## TODO: ROS params define a location for this
                AP.status = 'Standby'
                return 'wait'

class Wait(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success','error'], input_keys=[], output_keys=[])
    def execute(self, userdata):
        state = wait_for_start()
        return str(state)


class PickFromRoboticStation(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success','error'], input_keys=[], output_keys=[])

    def execute(self, userdata): # userdata has the growth_module.ID
        if AP.status == 'Busy':
            print('Automated platform is already doing a job')
            return 'error'
        elif AP.position != RS_position: # i.e, the automated platform is not in the proper location
            print('Automated platform is not in the correct position')
            return 'error'
        else:
            moving_result = pick()
            if check_for_safety_error():
                wait_for_solve(reason = 'safety')
                return 'error'
            else:
                AP.loaded = True
                RS.growthModuleCount -=1 ## TODO: Track which growth module space is unloaded
                self.status = 'Free'
                return 'go_to_growth_module'

class DepositShelf(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['success','error'], input_keys=[], output_keys=[])

    def execute(self, userdata): # userdata has the growth_module.ID
        if shelf.occupancy(userdata) == True:
            print('Growth Module in this location is already there')
            return 'error'
        elif AP.position != userdata: # i.e, the automated platform is not in the proper location
            print('Automated platform is not in the correct position')
            return 'error'
        else:
            moving_result = pick()
            if check_for_safety_error():
                wait_for_solve(reason = 'safety')
                return 'error'
            else:
                AP.loaded = False
                AP.status == 'Standby'
                shelf.occupancy= 1
                return 'go_to_home_position'


def main():
    rospy.init_node('GrowBotHub')
    sm = smach.StateMachine(outcomes=['finished'])     # Create a SMACH state machine

    with sm:

        smach.StateMachine.add('Init', Initialization(), transitions={'start_homing': 'Homing'}, remapping={})
        smach.StateMachine.add('Homing', Homing(), transitions={'success': 'Homing', 'error': 'Init'}, remapping={})
        rospy.sleep(10)
        sis = smach_ros.IntrospectionServer('server_name', sm, '/GrowBotHubProcess') # Create and start the introspection server
        sis.start()

        outcome = sm.execute()  # Execute SMACH plan
        rospy.spin()
        sis.stop()

""" LISTENER """
if __name__ == '__main__':
    main()
