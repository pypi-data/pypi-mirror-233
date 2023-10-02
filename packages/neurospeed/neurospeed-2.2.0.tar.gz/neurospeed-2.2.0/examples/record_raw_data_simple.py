# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 13:42:26 2021

@author: NeuroBrave



this code is a working axample of how to operate the built-in raw data recorder at NeuroSpeed.io

the code performs 4 main tasks:
    
    1. authentication in the neurospeed.io system with user and password
    
    2. starting and stopping the recorder: 
    
    3. running the data exporter (that converts the recording into downloadable .csv file)
    
    4. donwloading the recording file
    
    
    
    there are plenty of configuration options for the recorder, see the comments within the code.

"""


from pathlib import Path
import os
from neurospeed.auth.auth_as_customer_handler import Auth_AS_Customer_handler
from neurospeed.utils.helper_service import UtilService
from neurospeed.macros import macros

global customer_auth
global username


    
def main():
    global customer_auth
    global recorder_handler
    global exporter_handler
    global username

    # load Customer configuration
    customer_config_path = os.path.join(str(Path().absolute()) ,"config","customer_config.json")
    customer_config = UtilService.load_config_file(customer_config_path)
    
    # Authenticate as customer
    customer_auth = Auth_AS_Customer_handler(customer_config)
    customer_auth.login()
    
    os.path.join(str(Path().absolute()) ,"neurospeed\\config","hia_config1.json")
    config_user1 = UtilService.load_config_file(os.path.join(str(Path().absolute()) ,"config","hia_config1.json"))
    username = config_user1["username"] # or set here another custom username



    # run data recorder: 
    recorder_name="mydata"
    recorder_id = macros.start_recording(customer_auth, config_user1, recorder_name)



    # ****************************************************** 
    # send some data here, empty recorders are not generating downloaded file!
    


    # run exporter of recorder data into downloadable .csv format: 
    # exporter configuration
    exporter_config =  {
        # name your exporter up to 128 chars
        "custom_name": "export me gently", 
        
         # start_timestamp_mode. values options: 
         # 1) "start" - from the first recorded timestamp.  
         # 2) "custom_value" - custom starting timestamp in seconds(!) . 
         # for example : "1629900352" or for better Accuracy "1629900352.11..." 
         # but not 162990035211" which is timestamp represented in miliseconds instead of seconds!
        "start_timestamp_mode": "start", 
        
         #  custom_start_timestamp required if "start_timestamp_mode" is "custom_value"
        # "custom_start_timestamp": 1629900352.11111, 
        
        # end_timestamp_mode. values options:
        # 1) "end" - until the last recorded timestamp  
        # 2) "custom_value" - custom end timestamp in seconds(!). same logic as "start_timestamp_mode"
        # 3) interval_minutes - interval in minutes. set
        "end_timestamp_mode": "end", 
        
        # custom_timestamp_interval required if "end_timestamp_mode" is "interval_minutes", 
        #"custom_timestamp_interval": 3 ,
        
        # custom_end_timestamp required if "end_timestamp_mode" is "custom_value", 
       # "custom_end_timestamp": "1629900353.11111", 
       
       # to exporting specific streams, add their stream_id into the array.  
       # to exporting all recorded streams skip this configuration
       # "stream_ids": ["stream_id1", "stream_id2"]
    }
    save_folder = os.getcwd()
    download_filepath = macros.download_data(customer_auth, recorder_id, exporter_config, config_user1, save_folder)
    print(f"downloaded file: {download_filepath}")

if __name__ == '__main__':    
    main()  