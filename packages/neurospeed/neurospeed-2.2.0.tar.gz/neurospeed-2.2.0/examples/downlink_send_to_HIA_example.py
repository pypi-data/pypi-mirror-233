# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 12:32:58 2021

@author: NeuroBrave LTD


this code is an example application that performs the following:
    
    1. connects to NeuroSpeed.io cloud with "customer level" authentication (customer level is admin level which is higher than user level)
    2. listens to user's connect/disconnect events under that customer
    3. when user connects, uses the SSR Downlink protocol to send an arbitrary message string to the newly connected machine.
    
"""

import time
from neurospeed.auth.auth_as_customer_handler import Auth_AS_Customer_handler
from neurospeed.api_http_handlers.gateway_http_handler import Gateway_HttpHandler 
from neurospeed.utils.helper_service import UtilService
from neurospeed.api_socket_handlers.customer_room_handler import CustomerRoom_Handler
from neurospeed.api_socket_handlers.downlink_room_as_customer_handler import DownlinkRoom_AS_Customer_Handler

global customer_auth


# listen on connected hia events and send downlink message to connected user machine
def external_hia_device_connection_handler(event):
    global customer_auth

    username = event["username"]
    hia_id = event["hia_id"]
    sensors = event["sensors"]
    stream_ids = list(sensors.keys())
    print('external_hia_device_connection_handler event from User: {}, HIA: {} Stream_ids: {}'.format(username ,hia_id, stream_ids ))
    
    # Example connect to user machine with SSR_Socket downlink. SSRsocket allows downlink between customer and user on any machine. 
    downlinkRoom = DownlinkRoom_AS_Customer_Handler(customer_auth, username)
    downlinkRoom.connect()
    time.sleep(3)
    if downlinkRoom.is_connected():
        message = "hello user {}".format(username) 
        print("sending downlink message from customer")
        downlinkRoom.route_message(message)
    
    time.sleep(2)
    downlinkRoom.disconnect()
       

def external_hia_device_disconnect_handler(event):
    global customer_auth

    username = event["username"]
    hia_id = event["hia_id"]
    sensors = event["sensors"]
    stream_ids = list(sensors.keys())
    print('external_user_device_disconnect_handler event from User: {}, HIA: {} Stream_ids: {}'.format(username ,hia_id, stream_ids ))

        

# Hint: you can set "Verbose_socket_log": "True" in customer config to enable more logging
def main():
    global customer_auth
    
    # load customer config file
    customer_config = UtilService.load_config_file('config/customer_config.json')
    
    # Authenticate as customer
    customer_auth = Auth_AS_Customer_handler(customer_config)
    customer_auth.login()

    # connect to 'CustomerRoom_Handler', and listen on events across all users
    customerRoom = CustomerRoom_Handler(customer_auth)
    customerRoom.set_hia_connection_external_handler(external_hia_device_connection_handler)
    customerRoom.set_hia_disconnect_external_handler(external_hia_device_disconnect_handler)
    customerRoom.connect()
 
    

if __name__ == '__main__':    
    main()  