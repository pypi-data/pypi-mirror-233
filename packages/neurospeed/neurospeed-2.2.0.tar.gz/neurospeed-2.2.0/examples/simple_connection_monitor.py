
# -*- coding: utf-8 -*-
"""
@author: NeuroBrave
this code  is distributed under BSD licence.

this code requires: 
    active internet conenction 
    subscription to NeuroSpeed.io service.
    active EEG stream from neuroSpeed cloud.
"""

import time
from pathlib import Path
import os
from neurospeed.auth.auth_as_user_handler import Auth_AS_User_Handler
from neurospeed.api_socket_handlers.user_room_as_user_handler import UserRoom_AS_User_Handler
from neurospeed.utils.helper_service import UtilService
import socket
import json

from lib import send_email

global previous_message
global alert_message_sent
alert_message_sent = False
previous_message= None

global user_auth
bad_channel_statistics={}
def EEG_processing_handler1(payload):
    '''
    this function extracts data from payload each time a packet is received - typically 1 packet every second.
    Parameters
    ----------
    payload : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    example payload["output"] structure:
        {'heart_rate': {'estimated_heart_rate': 59.53488372093023}, 'ICA': {'artifact_detected': 0, 'artifact_power': -1}, 'bad_channel': [0, 0, 0, 0], 'engagement_upgraded_index_h-b': {'hard_decision': 2, 'soft_decision_v1': 2, 'soft_decision_v2': 2}, 'focus_attention_manf_index_h-p': {'hard_decision': 2, 'soft_decision_v1': 2, 'soft_decision_v2': 2}, 'focus_attention_upgraded_index_h-p': {'hard_decision': 2, 'soft_decision_v1': 2, 'soft_decision_v2': 2}, 'focus_attention_manf_index_h-b': {'hard_decision': 0, 'soft_decision_v1': 0, 'soft_decision_v2': 0}, 'engagement_upgraded_index_h-p': {'hard_decision': 0, 'soft_decision_v1': 0.012534856796264648, 'soft_decision_v2': 0.025069713592529297}, 'focus_attention_upgraded_index_h-b': {'hard_decision': 0, 'soft_decision_v1': 0, 'soft_decision_v2': 0}}

    example  payload["sensor_info"] structure: 
    
    '''
     

    # EEG_sensor_information = {}
    # EEG_sensor_information["EEG_channel_names"] = payload["sensor_info"]["channel_map"]
    # EEG_sensor_information["EEG_channel_num"] = len(payload["sensor_info"]["channel_map"])    
    # EEG_sensor_information["sampling_frequency"] = payload["sensor_info"]["sampling_frequency"]
    # print(EEG_sensor_information)

    print("got EEG packet")
    # print(payload["output"])
    
    # print(payload["output"]['bad_channel'])
      
def ppg_handler_func(payload):
    # print(payload["output"]["heart_rate_ppg"])
    pass
    

def EEG_processing_handler2(payload):
    # your implementation
    # print('EEG_processing_handler2')
    print(payload["output"].keys())
    pass
    
def customer_gamepad_msg_handler_function(payload):
    # your implementation
    print('customer_gamepad_msg_handler_function')
    pass

def customer_user_data_msg_handler_function(payload):
    # your implementation
    print('customer_user_data_msg_handler_function')
    pass


def report_missed_messages(email_msg = ''):
    print("message stream timout detected, sending alert")
    email_subj = "neurospeed disconnect alert"
    
    email_attachment_files = []
    # this function alerts user about broken data stream
    send_email.send_mail(send_from = 'oleg@neurobrave.com', send_to = 'oleg@neurobrave.com',
        subject = email_subj, message = email_msg, files=email_attachment_files,
        server = 'mail.smtp2go.com', port = 2525, username = "neurobrave", password="qibXXC603NzwZrFc")
    

def smartwatch_handler_func(payload):
    global previous_message
    global alert_message_sent
    alert_message_sent = False
    previous_message = time.time()
    print(payload["data"])
    
generic_handler = { # allows multiple handlers for each device
    'eeg': [ EEG_processing_handler1, EEG_processing_handler2],
    'gamepad': [customer_gamepad_msg_handler_function],
    'user_data': [customer_user_data_msg_handler_function],
    'ppg': [ppg_handler_func],
    'smartwatch': [smartwatch_handler_func]
}


def user_data_external_handler(payload):
    username = user_auth.get_username()
    stream_id = payload["stream_id"]
    device_type = payload["device_type"]
    hia_id = payload["hia_id"]
    sensor_info = payload["sensor_info"]
    # print("data from user: {} hia: {} stream_id: {} device_type: {}".format(username, hia_id, stream_id, device_type))
    print(".", end='')
    # execute each function handler for relevant device_type
    device_type = payload["device_type"].lower()
    handler_functions = generic_handler[device_type]
    for func in handler_functions:
        func(payload)
    
# see README(4) for payload structure  
def user_device_event_external_handler(payload):
    print('event: ', payload)  
    if payload["type"] =="disconnect": 
        report_missed_messages(f"client {payload['hia_id']} for user {payload['username']} disconnect from sensor detected!")
        
    


# Hint: you can set "Verbose_socket_log": "True" in user config to enable more logging
def main():
    global user_auth
    global previous_message
    global alert_message_sent
    config_user1 = UtilService.load_config_file(os.path.join(str(Path().absolute()) ,"config\\","hia_config.json"))
    # Authenticate as user
    user_auth = Auth_AS_User_Handler(config_user1)
    user_auth.login()

    userRoom = UserRoom_AS_User_Handler(user_auth)
    userRoom.set_data_external_handler(user_data_external_handler)
    userRoom.set_device_events_external_handler(user_device_event_external_handler)

    userRoom.connect()

    previous_message = time.time()
    timeout = 15 #seconds
    last_printed_msg = previous_message
    alert_message_sent = False
    while True:
        if last_printed_msg != previous_message:
            print(f"last msg received {previous_message}")
            last_printed_msg = previous_message
        if time.time() - previous_message > timeout: 
            if not alert_message_sent:
                report_missed_messages("missed packets from sensor detected!")
                alert_message_sent = True
        time.sleep(0.5)

if __name__ == '__main__':    
    main()  