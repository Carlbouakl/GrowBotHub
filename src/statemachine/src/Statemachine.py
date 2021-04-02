#!/usr/bin/env python3.7
import os
import numpy as np
import rospy
import smach
import smach_ros
import SHELF as shelf
import AUTOMATEDPLATFORM as AP
import GROWTHMODULE as growth_module
import ROBOTICARM as RS # Robotic Station

## TODO: create check_for_safety_error service on ROS
## TODO: create a move function
## TODO: Add state for switching growth module from one location to another

home_position = rospy.get_param('HOMEPOSITION')

class Initialization(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['start_homing'], input_keys=[], output_keys=[])

    def execute(self, userdata):
        userdata.test = rospy.get_param('TARE_WEIGHT') # Load parameters and classes here

        # handle safety errors that are present on startup
        if check_for_safety_error():
            wait_for_solve(reason='safety')

        return ('start_homing')


class Homing(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success','error'], input_keys=[], output_keys=[])

    def execute(self):
        moving_result = move(home_position)
        if check_for_safety_error():
            wait_for_solve(reason = 'safety')
            return ('repeat_homing')

        elif moving_result == 'Paused':
            wait_for_solve(reason='pause')
            return ('repeat_homing')

        elif moving_result != 'The position is reached':
            wait_for_solve(reason= 'moving_service_error')
            return ('repeat_homing')
        else:
            wait_for_start()
            AP.Pose = home_position
            return ('go_to_growth_module') # TODO: Rename this accroding to what the name of the next state is


class GoToGrowthModule(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['success','error'], input_keys=[], output_keys=[])

    def execute(self, userdata): # userdata has the growth_module.ID and the location you want to go to
        if shelf.Occupancy(userdata.ID) == False:
            print('Growth Module in this location does not exist')
            return 'error'
        elif AP.Status == 'Busy':
            print('Automated platform is already doing a job')
            return 'error'
        elif userdata.pose > shelf.Dimension:
            print('Growth module outside the shelf')
            return 'error'
        else:
            moving_result = move(growth_module.Location(userdata)) ## TODO: Put the coordinates of the growth Module
            if check_for_safety_error():
                wait_for_solve(reason = 'safety')
                return 'error'
            else:
                AP.Pose = growth_module.Location(userdata)
                return'pick_growth_module'


class PickGrowthModule(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['success','error'], input_keys=[], output_keys=[])

    def execute(self, userdata): # userdata has the growth_module.ID
        if shelf.Occupancy(userdata) == False:
            print('Growth Module in this location does not exist')
            return 'error'
        elif AP.Pose != userdata: # i.e, the automated platform is not in the proper location
            print('Automated platform is not in the correct position')
            return 'error'
        if AP.Loaded == 1:
            print('Automated Platform is already carrying a Growth Module')
            return 'error'
        else:
            moving_result = pick()
            if check_for_safety_error():
                wait_for_solve(reason = 'safety')
                return 'error'
            else:
                AP.Loaded == 1
                AP.Status == 'Moving'
                shelf.Occupancy(userdata) = 0
                return 'go_to_robotic_station'

class GoToRoboticStation(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['success','error'], input_keys=[], output_keys=[])

    def execute(self, userdata): # userdata has the growth_module.ID
        if AP.Loaded == 0:
            print('Automated Platform is not carrying a Growth Module')
            return 'error'
        elif AP.Pose != userdata: # i.e, the automated platform is not in the proper location ## TODO: Check for positon, not userdata
            print('Automated platform is not in the correct position')
            return 'error'
        elif RS.Status == 'Busy':
            print('Robotic Station does not have space for an additional growth module')
            return 'error'
        else:
            moving_result = pick()
            if check_for_safety_error():
                wait_for_solve(reason = 'safety')
                return 'error'
            else:
                AP.Pose = RS_position ## TODO: ROS params define a location for this
                return 'deposit_roboti_station'

class DepositRoboticStation(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['success','error'], input_keys=[], output_keys=[])

    def execute(self, userdata): # userdata has the growth_module.ID
        if RS.Status == 'Busy':
            print('Robotic Station does not have space for an additional growth module')
            return 'error'
        elif AP.Pose != RS_position: # i.e, the automated platform is not in the proper location
            print('Automated platform is not in the correct position')
            return 'error'
        else:
            moving_result = deposit()
            if check_for_safety_error():
                wait_for_solve(reason = 'safety')
                return 'error'
            else:
                AP.Pose = RS_position ## TODO: ROS params define a location for this
                AP.Status = 'Standby'
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
        if AP.Status = 'Busy':
            print('Automated platform is already doing a job')
            return 'error'
        elif AP.Pose != RS_position: # i.e, the automated platform is not in the proper location
            print('Automated platform is not in the correct position')
            return 'error'
        else:
            moving_result = pick()
            if check_for_safety_error():
                wait_for_solve(reason = 'safety')
                return 'error'
            else:
                AP.Loaded = True
                RS.NbrGrowthModules = RS.NbrGrowthModules - 1 ## TODO: Track which growth module space is unloaded
                self.Status = 'Free'
                return 'go_to_growth_module'

class DepositShelf(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['success','error'], input_keys=[], output_keys=[])

    def execute(self, userdata): # userdata has the growth_module.ID
        if shelf.Occupancy(userdata) == True:
            print('Growth Module in this location is already there')
            return 'error'
        elif AP.Pose != userdata: # i.e, the automated platform is not in the proper location
            print('Automated platform is not in the correct position')
            return 'error'
        else:
            moving_result = pick()
            if check_for_safety_error():
                wait_for_solve(reason = 'safety')
                return 'error'
            else:
                AP.Loaded == 0
                AP.Status == 'Standby'
                shelf.Occupancy(userdata) = 1
                return 'go_to_home_position'


def main():
    rospy.init_node('GrowBotHub')
    sm = smach.StateMachine(outcomes=['finished'])     # Create a SMACH state machine

    with sm:

        smach.StateMachine.add('Init', Initialization(),
                               transitions={'start_homing': 'Homing'}, remapping={})
        smach.StateMachine.add('Homing', Homing(),
                               transitions={'repeat_homing': 'go_to_growth_module'}, remapping={})

       sis = smach_ros.IntrospectionServer('server_name', sm, '/GrowBotHubProcess') # Create and start the introspection server
       sis.start()

       outcome = sm.execute()  # Execute SMACH plan
       rospy.spin()
       sis.stop()


""" LISTENER """
if __name__ == '__main__':
    main()
