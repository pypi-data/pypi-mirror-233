
# -*- coding: utf-8 -*-
"""
@author: NeuroBrave
this code  is distributed under BSD licence.

this code requires: 
    active internet conenction 
    subscription to NeuroSpeed.io service.
    active EEG stream from neuroSpeed cloud.
"""


from pathlib import Path
import os
from neurospeed.auth.auth_as_user_handler import Auth_AS_User_Handler
from neurospeed.api_socket_handlers.user_room_as_user_handler import UserRoom_AS_User_Handler
from neurospeed.utils.helper_service import UtilService

import socket
import json

#the following imports needed only to operate NeuroSpeed.IO cloud recorder:
from neurospeed.auth.auth_as_customer_handler import Auth_AS_Customer_handler
from neurospeed.macros import macros
import time


global user_auth


UDP_IP="127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def EEG_processing_handler(payload):
    '''
    this function extracts data from payload each time a packet is received - typically 1 packet every second.
    Parameters
    ----------
    payload : dictionary with values of raw sensor data, processed information and processing parameters.

    Returns
    -------
    None.

    payload structure: see file "eeg_payload.json"


    example  payload["sensor_info"] structure: 
    	{
		'id': 6461,
		'device_type': 'eeg',
		'sensor_id': '9LUMVF'
		'stream_id': 'EEG_9LUMVF_0',
		'is_attached': True,
		'sensor_version': 1, 
		'stream_state': 'enabled',
		'channels_count': 4,
		'created_at': '2022-06-01T14:13:49.926Z',
		'channel_map': ['TP9', 'AF7', 'AF8', 'TP10', 'timestamp'], 
		'buffer_length': 1,
		'manufacturer_id': 'muse',
		'sampling_frequency': 256, 
		'buffer_length_samples': 256,
		'buffer_length_seconds': 1
		}
 
    '''
   
    # to get raw sensor data:
    # raw_data = payload["data"]["sample"]        #returns list with 256 entries, each entry is list of 5 values: 4 channel voltages and a timestamp
    
    #to get cleaned raw data: 
    # cleaned_data = payload["output"]["raw_data"]["clean"]   #returns list with 256 entries, each entry is list of 4 values: 4 channel voltages 

    #to get neuro-marker data:         
    # marker_name = 'engagement_upgraded_index_h-b'
    # marker_data = payload["output"][marker_name]   #returns dictionary {'hard_decision': <int>, 'soft_decision_v1': <float>, 'soft_decision_v2': <float>},

    # #to get channel health indicators: 
    # bad_channel = payload["output"]['bad_channel'] #returns list with 4 entries, each entry is an integer: 0 if channel is good, 1 if channel is bad.

    print("received NeuroSpeed data packet")

    output_packet = {}
    output_packet["clean_data"] = payload["raw_data"]["clean"] 
    output_packet["brainwave_power"] = payload["output"]["brainwave_power"]
    output_packet["engagement_upgraded_index_h-b"] = payload["output"]["engagement_upgraded_index_h-b"]
    output_packet["focus_attention_upgraded_index_h-b"] = payload["output"]["focus_attention_upgraded_index_h-b"]
    output_packet["engagement_level_digital_media_upgraded_h-b"] = payload["output"]["engagement_level_digital_media_upgraded_h-b"]
    output_packet["bad_channel"] = payload["output"]["bad_channel"]
    # print(payload) 

    to_send = str(output_packet).encode('utf-8')
    if len(to_send) > 65000:
        print("UDP packet size exceded, not sending")
    else:
        sock.sendto(to_send, (UDP_IP, UDP_PORT))
    
    

generic_handler = { # allows multiple handlers for each device
    'eeg': [ EEG_processing_handler],
    'gamepad': [],
    'user_data': [],
    'ppg': [],
    'keyboard':[]
}



def user_data_external_handler(payload):
    username = user_auth.get_username()
    print("data from user: {} hia: {} stream_id: {} device_type: {}".format(username, payload["hia_id"], payload["stream_id"], payload["device_type"]))
    
    # execute each function handler for relevant device_type
    device_type = payload["device_type"].lower()
    handler_functions = generic_handler[device_type]
    for func in handler_functions:
        func(payload)
    
# see README(4) for payload structure  
def user_device_event_external_handler(payload):
    print('event: ', payload)
    if payload["type"] =="disconnect": 
        print(f"client {payload['hia_id']} for user {payload['username']} disconnect from sensor detected!")
    if payload["type"] =="connect": 
        print(f"client {payload['hia_id']} for user {payload['username']} disconnect from sensor detected!")
        



# Hint: you can set "Verbose_socket_log": "True" in user config to enable more logging
def main():
    
    
    #the following code is used to connect to user-level API to subscribe to data stream:
    global user_auth
    config_user1 = UtilService.load_config_file(os.path.join(str(Path().absolute()) ,"config\\","hia_config.json"))
    # Authenticate as user
    user_auth = Auth_AS_User_Handler(config_user1)
    user_auth.login()

    userRoom = UserRoom_AS_User_Handler(user_auth)
    userRoom.set_data_external_handler(user_data_external_handler)
    
    # the following 2 lines of code are optional: subscribe to connect/disconnect events to manage related events:
    userRoom.set_device_events_external_handler(user_device_event_external_handler)
    userRoom.connect()


    # this optional chunk of code is used to start the data recorder on neurospeed.io
    with open('config/dashboard_credentials.json') as f:
         customer_config = json.load(f)             
    # Authenticate as customer on neurospeed.io:
    print(f"using customer config {customer_config}")
    customer_auth = Auth_AS_Customer_handler(customer_config)
    login_success = customer_auth.login()
    
    if not login_success:
        print("Failed to log in as Customer")
    else:
        print("logged in as Customer, initiating recorder")
        recording_name  = "my_recording"
        recorder_id = macros.start_recording(customer_auth, config_user1, recorder_name = recording_name)
    
    
    
        time.sleep(60)
        
        
        
        
        # stop the data recording on the cloud. Stopping the recording does not automatically download the data, another command does it.
        macros.stop_recording(recorder_id)
     
        # command the cloud engine to perform the data export and download the datafile:  
            
        # "exporter" finalizes the recording, converts it to human-readable .csv file and makes it available for download:
        # exporter name can be any string. exporter can export certain range of the recording, by selecting start and end timestamps. 
        # to export the entire recording, use: "start_timestamp_mode": "start", "end_timestamp_mode": "end"
     
        exporter_config =  {"custom_name": recording_name + "_exported",    
        "start_timestamp_mode": "start", 
        "end_timestamp_mode": "end"}
        
        save_folder =  os.getcwd()        
        exporter_filename = macros.download_data(customer_auth, recorder_id, exporter_config, config_user1, save_folder)
        
        
    
   

if __name__ == '__main__':    
    main()  