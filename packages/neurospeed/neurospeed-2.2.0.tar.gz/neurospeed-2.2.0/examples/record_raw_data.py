# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 13:42:26 2021

@author: NeuroBrave



this code is a working axample of how to operate the built-in raw data recorder at NeuroSpeed.io

the code performs 4 main tasks:
    
    1. authentication in the neurospeed.io system with user and password
    
    2. starting and stopping the recorder: 
        recorder is set up and records for 15 seconds,
        then it's paused for 5 seconds, 
        then reactivated for another 5 seconds, 
        then finally stopped.
        there's an option to delete the recorder after recording. Do not delete the recording before it's data has been exported using the exporter.
    
    3. running the data exporter (that converts the recording into downloadable .csv file)
    
    4. donwloading the recording file
    
    
    
    there are plenty of configuration options for the recorder, see the comments within the code.

"""

import time
from pathlib import Path
import os
from neurospeed.auth.auth_as_customer_handler import Auth_AS_Customer_handler
from neurospeed.api_http_handlers.recorder_http_handler import UserRoom_Recorder_Handler
from neurospeed.api_http_handlers.exporter_http_handler import UserRoom_Recorder_Exporter_Handler
from neurospeed.utils.helper_service import UtilService

import urllib.request

global customer_auth
global recorder_handler
global exporter_handler
global username


def run_recorder_flow():
    global recorder_handler
    global username
    # create recorder. recorder created with status "resource_pending". once available recording resources found and assgined
    # recorder status will change to "pending", then once recorder picked by assigned recorder resources and start to record status will change to "recording"

    recorder = recorder_handler.create_recorder(username)
    recorder_id = str(recorder["id"])
    print('created recorder with id', recorder_id)
    
    recorder = recorder_handler.get_recorder(recorder_id)     
    print("recorder status: " + recorder["status"])
    
    recorder_recording = False
    max_query_attemps = 10
    query_attemps = 1
    while (recorder_recording != True & (query_attemps < max_query_attemps) ):
        recorder = recorder_handler.get_recorder(recorder_id)   
        print("recorder status: " + recorder["status"])
        if (recorder["status"] == "recording"):
            print('recorder started recording')
            recorder_recording = True
        else:
            print('recorder not recording yet')
            query_attemps = query_attemps + 1
            time.sleep(3)
             
    if (recorder_recording != True):
        print('recorder not yet recording after ' + str(query_attemps)  + ' query attempts')
        recorder_handler.delete_recorder(recorder_id)
        return
    
    
    print('~~~~~~~~~~~~~~~~~~')
    
    recording_duration = 20
    time.sleep(recording_duration-5)

    #once recorder starts recording, you can change it's status to paused or stopped. you can resume paused recorder but not stopped recorder
    # pause recorder for 5 seconds:
    res = recorder_handler.update_recorder(recorder_id, "paused")
    recorder = recorder_handler.get_recorder(recorder_id)     
    print("recorder status: " + recorder["status"])
    time.sleep(5)
    
    # reactivate paused recorder and add another 5 seconds to the recording
    recorder_handler.update_recorder(recorder_id, "pending") 
    recorder = recorder_handler.get_recorder(recorder_id)     
    print("recorder status: " + recorder["status"])
    
    time.sleep(5)
    
    recorder_handler.update_recorder(recorder_id, "pending") 
    recorder = recorder_handler.get_recorder(recorder_id)     
    print("recorder status: " + recorder["status"])
    
    
    recorder_handler.update_recorder(recorder_id, "stopped") 
    #recorder_handler.delete_recorder(recorder_id) # uncomment this to delete recorder
    recorders = recorder_handler.list_recorders(username)
    print(recorders)
    
    return recorder_id


def run_exporter_flow(recorder_id, exporter_config):
    global exporter_handler
    
    # create exporter, if recorder has no data, request will fail.
    exporter = exporter_handler.create_exporter(recorder_id, exporter_config)
    exporter_id = str(exporter["id"])
    
    # once exporter created, query it's status until it "exported".
    exporter_exported = False
    max_query_attemps = 20
    query_attemps = 1
    while (exporter_exported != True & (query_attemps < max_query_attemps) ):
        exporter = exporter_handler.get_exporter(exporter_id)   
        print("exporter status: " + exporter["status"])
        if (exporter["status"] == "exported"):
            print('exporter finished exporting')
            exporter_exported = True
        else:
            print('exporter not yet exported the files')
            query_attemps = query_attemps + 1
            time.sleep(10)
             
    if (exporter_exported != True):
        print('exporter not yet exported the file after  ' + str(query_attemps)  + ' query attempts')
        exporter_handler.delete_exporter(exporter_id)
        return
   
    # once exporter exported the file, you can ask for an URL to download the exported file. 
    #the url available for only short time before it deprecates
    url_response = exporter_handler.get_exported_url(exporter_id)
    
    
    time.sleep(2)
   #delete_exporter(exporter_id) # uncomment this to delete exporter
    time.sleep(1)
    # list all exporters under username
    exporters = exporter_handler.list_exporters(username)
    print(exporters)
    
    return url_response
    
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
    
    recorder_handler = UserRoom_Recorder_Handler(customer_auth)
    recorder_id = run_recorder_flow()
    print('RECORDER ID: {}'.format(recorder_id))



    # run exporter of recorder data into downloadable .csv format: 
    exporter_handler = UserRoom_Recorder_Exporter_Handler(customer_auth)

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
    download_url = run_exporter_flow(recorder_id, exporter_config) 

    try: 
        savefilename = "recording_save.csv"
        urllib.request.urlretrieve(download_url, savefilename)
    except: 
        print("couldn't download file")

if __name__ == '__main__':    
    main()  