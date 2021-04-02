#!/usr/bin/env python3.7

import os
import can

def initialize_motors(self):
    hex = rospy.get_param('CAN_INITIALIZE_MOTORS')
    self.canSendMessage(canMessage)

def move(self, position, id):   #TODO: Integrate in a class
    hexposition = self.hexSwapperTool(position)
    msg = str(hexposition) + canConfig.Post_Position_2 # '00001F00'
    arrayData = self.parseHex(msg)
    canMessage = can.Message(self, extended_id=False, arbitration_id=id, data=arrayData)
    self.canSendMessage(canMessage)

def pick(self):
    position = rospy.get_param('LINEAR_ACTUATION_EXTENTION')
    hexposition = self.hexSwapperTool(position)
    msg = str(hexposition) + canConfig.Post_Position_2 # '00001F00'
    arrayData = self.parseHex(msg)
    canMessage = can.Message(self, extended_id=False, arbitration_id=id, data=arrayData)
    self.canSendMessage(canMessage)

def deposit(self):  ## TODO: this is completely wrong, define it properly to deposit the growth module on the RS
    position = rospy.get_param('LINEAR_ACTUATION_EXTENTION')
    hexposition = self.hexSwapperTool(position)
    msg = str(hexposition) + canConfig.Post_Position_2 # '00001F00'
    arrayData = self.parseHex(msg)
    canMessage = can.Message(self, extended_id=False, arbitration_id=id, data=arrayData)
    self.canSendMessage(canMessage)

def canSendMessage(self, msg):
    try:
        self._bus.send(msg)

    except Exception as e:
        print("Sending CAN message failed")

def hexSwapperTool(self, value):
    hexValue = hex(value)
    hexValue = hexValue[hexValue.index('x')+1:]
    strValue = str(hexValue)
    length = len(strValue)
    for i in range(length, 8):
        strValue = '0' + strValue

    returnedValue = ''
    for i in range(1, 5):
        returnedValue = returnedValue+strValue[(8-2*i):(8-2*i+2)]
    return returnedValue

def parseHex(self, hexNumber):

    letters = ['A', 'B', 'C', 'D', 'E', 'F']
    a = []
    for i in range((len(hexNumber)/2)):
        twodigits = hexNumber[2*i:2*i+2]

        if twodigits[0] in letters:
            digit1 = letters.index(twodigits[0])+10
        else:
            digit1 = int(twodigits[0], 16)

        if twodigits[1] in letters:
            digit2 = letters.index(twodigits[1])+10
        else:
            digit2 = int(twodigits[1], 16)

        number = digit1*16 + digit2
        a.append(number)
    return a
