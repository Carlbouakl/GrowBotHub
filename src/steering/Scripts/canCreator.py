#!/usr/bin/env python

import os
import can
import string
import time
import canConfig
import rospy


class canCreator(can.Listener):
    def on_message_received(self, msg):
        pass

    def sendMovementMessage(self, position, id):
        hexposition = self.hexSwapperTool(position)
        msg = str(hexposition) + canConfig.Post_Position_2
        arrayData = self.parseHex(msg)
        canMessage = can.Message(self, extended_id=False, arbitration_id=id, data=arrayData)
        self.canSendMessage(canMessage)

    def sendVelocityMessage(self, velocity, id_Extra):
        hexvelocity = self.hexSwapperTool(velocity)
        msg = hexvelocity
        canMessage = can.Message(self, extended_id=False, arbitration_id=id_Extra, data=self.parseHex(msg))
        msg = hexvelocity
        canMessage = can.Message(self, extended_id=False, arbitration_id=id_Extra, data=self.parseHex(msg))
        self.canSendMessage(canMessage)

    def sendMessage(self, type, id):
        msg = []
        if type == 'disable':
            msg.append(canConfig.Disable_Message)

        if type == 'preMovement':
            msg.append(canConfig.Enabling_Motors_General)

        if type == 'initialiazition':
            msg.append(canConfig.Enabling_Motors_1)
            msg.append(canConfig.Enabling_Motors_2)
            msg.append(canConfig.Enabling_Motors_General)

        if type == 'ErrorReset':
            msg.append(canConfig.Reset_Errors)

        if type == 'Homing':
            msg.append(canConfig.Homing_Message_1)
            msg.append(canConfig.Homing_Message_2)
            msg.append(canConfig.Enabling_Motors_General)
            msg.append(canConfig.Homing_Message_4)

        for i in range(len(msg)):
            canMessage = can.Message(self, extended_id=False, arbitration_id=id, data=self.parseHex(msg[i]))
            self.canSendMessage(canMessage)
            time.sleep(0.1)

    def sendPretoOperational(self):
        canMessage = can.Message(self, extended_id=False, arbitration_id=self.id_PretoOperational, data=self.parseHex(canConfig.PreOperation_to_Operational))
        self.canSendMessage(canMessage)

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

    def canSendMessage(self, msg):
        try:
            self._bus.send(msg)
        except Exception as e:
            print('CAN interface is down')

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
