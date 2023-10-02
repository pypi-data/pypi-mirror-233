# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 13:42:26 2021

@author: NeuroBrave
"""


import time
from pathlib import Path
from neurospeed.auth.auth_as_customer_handler import Auth_AS_Customer_handler
from neurospeed.api_http_handlers.exporter_http_handler import UserRoom_Recorder_Exporter_Handler
from neurospeed.utils.helper_service import UtilService

import os
global customer_auth
global exporter_handler
global username


# once recorder has at least 1 packet recorded, you can create exporter to export data
# exporter which belongs to some recorder, must finish first before another exporter can be created for this recorder
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
    print(url_response)
    
    time.sleep(2)
   #delete_exporter(exporter_id) # uncomment this to delete exporter
    time.sleep(1)
    
    # list all exporters under username
    page_number = 1 
    page_size = 5 # max 100 rows per page
    exporters = exporter_handler.list_exporters(username, page_number, page_size)
    print(exporters)
    
    
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
    
    exporter_handler = UserRoom_Recorder_Exporter_Handler(customer_auth)
    
    
    recorder_id  = 12 # !!! set here the recorder_id 
    config_user1 = UtilService.load_config_file(os.path.join(str(Path().absolute()) ,"config","hia_config1.json"))
    username = config_user1["username"] # or set here another custom username
  
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
    run_exporter_flow(recorder_id, exporter_config) 


if __name__ == '__main__':    
    main()  