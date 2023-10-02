'''

this script starts cloud-based recorder on neursospeed,
sets experiment labels to create labeled data, 
sends some random raw data from 
and downloads the processed output files

the scripts expects a /config subfolder with following files:
    dashboard_credentials.json - for customer-level auth (to operate the recorder-exporter function)
        inside:
            {
            "email": "",
            "password": ""
            }
    
            
    HIA_config.json - for user-level auth (to send the data)
        inside: 
            {
                "account_id": "",
                "username": "",
                "user_password": "",
                "HIA_ID": "XYZ123",
                "Verbose_socket_log": "False"
            }
            
    optional: api_config.json (if exists, the neurospeed server address will be used from this file. useful for running on non-default neurospeed servers.)
    inside: 
            
           {
           "is_prod": "True", 
           "api_address_prod": "https://api.neurospeed.io",
           "api_address_local":  "http://localhost:3000",
           	"pipeline_address_prod": "wss://api.neurospeed.io",
           	"pipeline_address_local": "ws://localhost:3000",
           }
                 
'''
import json
import os
import sys
import time
import logging
from datetime import datetime

from neurospeed.auth.auth_as_user_handler import Auth_AS_User_Handler
from neurospeed.utils.helper_service import UtilService
from neurospeed.hia_user_data.neurobrave_sensor_interface import HIA_Client
from neurospeed.auth.auth_as_customer_handler import Auth_AS_Customer_handler
from neurospeed.macros import macros


def generate_sensor_info():
    '''
    this function generates sensor_info dictionary that is nesessary ot initialize the HIA client.
    input:
        none
    '''
    # generate  sensors stream ids
    
    sensor_info = dict()
    user_data_stream_id =  "user_data" + '_' + UtilService.generateId(6)
    sensor_info[user_data_stream_id] =  {
    "device_type": "user_data",
    "channel_count": 2,
    "sampling_frequency": 10,
    "buffer_length" : 1.0,  #data buffer length in seconds. 
    "manufacturer_id": "myCompanyName",
    "sensor_id" : user_data_stream_id,
    "stream_id": user_data_stream_id,
    "stream_state" : "enabled",
     "channel_map" : ["chanllel_0", "channel_1"]
    } 
    
    user_data_stream_id =  "some_custom_stream_id"
    sensor_info[user_data_stream_id] =  {
    "device_type": "user_data",
    "channel_count": 2,
    "sampling_frequency": 10,
    "buffer_length" : 1.0,  #data buffer length in seconds. 
    "manufacturer_id": "myCompanyName",
    "sensor_id" : user_data_stream_id,
    "stream_id": user_data_stream_id,
    "stream_state" : "enabled",
     "channel_map" : ["chanllel_0", "channel_1"]
     }

    return sensor_info


def disconnect_external_handler(hia_client):
    # this function is automatically executed when this client disconnects from NeuroSpeed cloud
    pass
    

# would be called for each hia after successfuly connection  
def connection_external_handler(hia_client):
    # this function is automatically executed when this client connects to NeuroSpeed cloud
    pass

def init_HIA_client(hia_config):
    
    '''
    this function  initializes the HIA client and connect the cloud streaming (upload raw data to neurospeed)
    
    input:
        config - dictionary with config for this epxeriment program 
        hia_config dictionary
        
    output 
        hia_user client object instance
        sensor info dictionary
    
    '''
    user1_auth = Auth_AS_User_Handler(hia_config)
    user1_auth.login()
    
    hia_sensor_info_user1 = generate_sensor_info() 
     
    logging.debug('Generated sensor info: {}'.format(hia_sensor_info_user1) )
    hia_user1 = HIA_Client(user1_auth, hia_sensor_info_user1)   
    hia_user1.set_socket_connection_external_handler(connection_external_handler)
    hia_user1.set_socket_disconnect_external_handler(disconnect_external_handler)
    logging.debug("HIA_ID: " + str(user1_auth.get_hia_id()))   
    hia_user1._device_type = "EEG"
    hia_user1.connect()
    return hia_user1, hia_sensor_info_user1

    
    
 

if __name__ == '__main__':


    todays_date = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    logfilename = "log"+todays_date+".txt"
    logfile = open(logfilename, "w")

        
    # datafolder, where to store the recorded data files locally:
    datafolder = "C:\\neurobrave"
    
    subject_name = "my_subject_1"
   
    hia_client = None 
    with open('config/hia_config.json') as f:
        hia_config = json.load(f)
 
    with open('config/dashboard_credentials.json') as f:
         customer_config = json.load(f)             
    # Authenticate as customer on neurospeed.io:
    print(f"using customer config {customer_config}")
    customer_auth = Auth_AS_Customer_handler(customer_config)
    customer_auth.login()

    
    recorder_id = macros.start_recording(customer_auth, hia_config, recorder_name = subject_name)
    
    

    max_hia_reconnect_retries = 3
    for reconnect_idx in range(max_hia_reconnect_retries):
        hia_client, hia_sensor_info = init_HIA_client(hia_config)
        if hia_client.is_connected():
            break
        else:
            logging.debug("HIA connection retrying...")
            time.sleep(3)
    
    if not hia_client.is_connected():
        logfile.write("FAILED connecting to cloud streaming!\n")
        sys.exit()
    


    # set the label for all the transmitted data from this point onwards:
    hia_client.set_label("experiment_part_1")
    
    # tranmsit some arbitrary data:
    datatype = "user_data"
    stream_id = list(filter(lambda x: x.startswith(datatype), list(hia_sensor_info.keys())))[0]

    for i in range(100):
        data = [[1,2,3,4,5,6,7,8,9,10], [1,2,3,4,5,6,7,8,9,10]]
        
        hia_client.send_data_direct(data, stream_id, send_without_timestamp=True, device_type=datatype)       
        time.sleep(0.2)
    
    
    # set the label for all the transmitted data from this point onwards:
    hia_client.set_label("experiment_part_2")



    for i in range(100):
        data = [[1,2,3,4,5,6,7,8,9,10], [1,2,3,4,5,6,7,8,9,10]]
        
        hia_client.send_data_direct(data, stream_id, send_without_timestamp=True, device_type=datatype)       
        time.sleep(0.2)
        

    # stop the data transmission:
        
    hia_client.disconnect()
    print("hia status: " + str(hia_client.is_connected()))   
    
    # stop the data recording on the cloud. Stopping the recording does not automatically download the data, another command does it.
    macros.stop_recording(recorder_id)
    

    # command the cloud engine to perform the data export and download the datafile:  
        
    # "exporter" finalizes the recording, converts it to human-readable .csv file and makes it available for download:
    # exporter name can be any string. exporter can export certain range of the recording, by selecting start and end timestamps. 
    # to export the entire recording, use: "start_timestamp_mode": "start", "end_timestamp_mode": "end"
 
    exporter_config =  {
    "custom_name": subject_name + "_exported",    
    "start_timestamp_mode": "start", 
    "end_timestamp_mode": "end"
    }
    
    save_folder =  os.path.join(os.getcwd(), datafolder)        
    exporter_filename = macros.download_data(customer_auth, recorder_id, exporter_config, hia_config, save_folder)
    
    
    logfile.close()
     
     