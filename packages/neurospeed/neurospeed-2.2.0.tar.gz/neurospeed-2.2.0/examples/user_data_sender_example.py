
import time
from pathlib import Path
import os

from neurospeed.auth.auth_as_user_handler import Auth_AS_User_Handler
from neurospeed.api_socket_handlers.downlink_room_as_user_handler import DownlinkRoom_AS_User_Handler
from neurospeed.utils.helper_service import UtilService
from neurospeed.hia_user_data.neurobrave_sensor_interface import HIA_Client

import threading


x= [12, 14]

my_custom_sensor_info = {
   'sensor_type': 'vehicle speed',
   'channel_count' : 2,
   'channel_map': ["ch1", "ch2", "timestamp"], # timestamp doesn't count as channel
   'manufacturer_id': 'toyota'

}

# see README(5)
def get_sensors_mockup():
    # generate SOME sensors stream ids
    user_data_stream_id =  "user_data" + '_' + UtilService.generateId(6)
    user_data_custom_stream_id = "some_custom_stream_id"

    sensor_info = dict()
    sensor_info[user_data_stream_id] =  {
        "device_type": "user_data",
        "channel_count": 2,
        "channel_map": ["ch_0", "ch1", "timestamp"], # timestamp doesn't count as channel
        "sensor_id" : user_data_stream_id,
        "stream_id": user_data_stream_id,
        "stream_state" : "enabled"
    } 
    
    sensor_info[user_data_custom_stream_id] =  {
        "device_type": "user_data",
        "channel_count": 2,
        "channel_map": ["ch_9",  "ch10", "timestamp"], # timestamp doesn't count as channel
        "sensor_id" : user_data_custom_stream_id,
        "stream_id": user_data_custom_stream_id,
        "stream_state" : "enabled"
    } 
    
    return sensor_info
 


def downlink_message_external_handler(downlink_handler_instance, payload):
    username = downlink_handler_instance.get_username()
    print('~~~external user', username,' downlink message: ', payload)


# send dummy data loop for some stream_id. must be activated after socket successful connection.
def generate_data(hia_client, stream_id):
    for i in range(5000):
        if hia_client.is_connected() == False: # stop sending data if disconnected
            raise ValueError("hia for " , hia_client.get_username(), " disconnected , stopping data generator thread")
        if hia_client.is_stream_enabled(stream_id): # send only if stream enabled for that sensor
            hia_client.send_data(x.copy(), stream_id)
        time.sleep(0.05)
        
    hia_client.disconnect() #disconnect after finish, just for the example


def disconnect_external_handler(hia_client):
   print("hia:[", hia_client.get_hia_id(),"]", "user:[", hia_client.get_username(),"] disconnected ")
    
 
    
# would be called for each hia after successfuly connection  
def connection_external_handler(hia_client):
    username = hia_client.get_username()
    hia_id = hia_client.get_hia_id()
    print('connected as ', username, " with hia: " ,hia_id, ". sending data..")
    
    # generate dummy data for each sensor inside HIA_Client, 
    sensor_info = hia_client.get_sensor_info()
    for stream_id in sensor_info:
        print("activating data generator thread for stream_id:", stream_id , " username: ", username, "hia_id: ", hia_id)
        user_data_data_generator = threading.Thread(target = generate_data, args=[hia_client, stream_id])
        time.sleep(0.1)
        user_data_data_generator.start()

    
def run_user_test_flow(config_path):
    # load user configuration
    user_config_path = os.path.join(config_path)
    user_config = UtilService.load_config_file(user_config_path)
    
    # create Auth_AS_User_Handler and pass user configuration 
    user_auth = Auth_AS_User_Handler(user_config)
    
    # login to NeuroSpeed as user
    user_auth.login()
    time.sleep(1)
    # get pre-defined sensor mockup information
    hia_sensor_info_user = get_sensors_mockup() 
    
    print('Generated mockup sensors for username: {}'.format(user_config["username"]))
    
    # create HIA instance and pass user's Auth_Handler along with generated sensors info
    hia_client = HIA_Client(user_auth, hia_sensor_info_user)
    
    # This is example for periodical sending of data from a thread
    
    # attach external handlers this external dis\connection handler would be called on dis\connection 
    hia_client.set_socket_connection_external_handler(connection_external_handler) 
    hia_client.set_socket_disconnect_external_handler(disconnect_external_handler)
    
    # connect via HIA_Client to NeuroSpeed Pipeline 
    hia_client.connect()
    ## once connection established, "connection_external_handler" function would be called and result in mockup data generation 
    
    
    # example connecting to SSR downlink and listen on events from customer
    user_downlink = DownlinkRoom_AS_User_Handler(user_auth)
    user_downlink.set_downlink_router_external_handler(downlink_message_external_handler)
    user_downlink.connect()
    
    
    # This example of simple manual data sender:
    time.sleep(5) 
    if hia_client.is_connected():
        first_stream_id = next(iter(hia_sensor_info_user)) # take first stream_id for the example
        hia_client.set_label("welcome")      
        time.sleep(5)
        hia_client.set_label("goodbye")
  
    hia_client.disconnect()
    
# example of login, connect and send data as 2 different HIA users with 2 mockup sensors for each
# Hint: you can set "Verbose_socket_log": "True" in user config to enable more logging
def run_HIAs():
    
    config_path_user1 = os.path.join(str(Path().absolute()) ,"config","hia_config.json")
    run_user_test_flow(config_path_user1)
    
  #  config_path_user2 = os.path.join(str(Path().absolute()) ,"config","hia_config2.json")
   # run_user_test_flow(config_path_user2)


if __name__ == '__main__':    
    run_HIAs()