#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import rospy
import time
import can
import time
import threading
import canCreator
import canConfig
import os
home_directory = os.getenv("HOME")

class Safety(canCreator.canCreator):
    def __init__(self):
        self._bus = can.interface.Bus(channel=canConfig.CAN_CHANNEL, bustype=canConfig.CAN_TYPE)
        self.error_type = ['Emergency Button', 'No Error']
        self._listeners = [self]
        self._notifier = can.Notifier(self._bus, self._listeners)
        self.es = None
        self.error_msg = ' '
        self.error_msg_18 = 'No Error'
        self.cnt = 0

        toSend = ['00000100', '00000010', '00000000']
        self.handle_message_sending(toSend)

        thread = threading.Thread(target=self.reset_errors)
        thread.daemon = True
        thread.start()

    def on_message_received(self, msg):

        ID = hex(msg.arbitration_id)[2:]
        ID = ID.upper()

        Decimal = msg.data[0]  # takes 1 byte and transforms it to decimal
        Binary = bin(Decimal)  # Transform the 1 byte decimal value to binary
        String = str(Binary)
        String = String[2:]


        if ID == '18A':
            self.es = int(str(Binary[len(Binary)-3]))
            String1 = String
            for i in range(8-len(String1)):
                String1 = '0' + String1

            for i in range(2, 7):
                if String1[i] == '1':
                    self.error_msg_18 = self.error_type_18[i]
                elif String1[2:7] == '00000':
                    self.error_msg_18 = self.error_type[8]
                    self.cnt = 0
                    self.error_msg = self.error_type[8]

        if ID == '28A':
            String2 = String
            for i in range(8 - len(String2)):
                String2 = '0' + String2
            print 'ID =28A   ' + str(String2)
            if len(String2) == 8:
                for i in range(len(String2)):
                    if String2[i] == '1':
                        self.error_msg = self.error_type[i]

                    elif String2 == '00000000':
                        self.error_msg = ' '

        if self.error_msg == ' ' and self.error_msg_18 == self.error_type_18[5]:
            self.error_msg = 'Emergency button pushed'


    def handle_message_sending(self, toSend):
        for i in range(len(toSend)):
            toSend[i] = "0x{:02x}".format(int(toSend[i], 2))[2:]
            canMessage = can.Message(self, extended_id=False, arbitration_id=522, data=self.parseHex(toSend[i]))     # 20A corresponds to 522 decimal
            self.canSendMessage(canMessage)
            time.sleep(0.5)

    def send_message(self):
        print self.current_error, ' printing current error'
        os.system('echo robotics | sudo -S ip link set down can1')

        if self.current_error[0] == '1' or self.current_error[1] == '1':
            toSend = ['00000100','00000010','00000000' ]
