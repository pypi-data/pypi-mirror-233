#  copyright 2020 NeuroBrave LTD
#simple API for handling SSR's (sensor side reactor) events that are
# pushed from the NB client as a result of user's interaction with the processing routines



from pathlib import Path
import time
import os

from neurospeed.auth.auth_as_user_handler import Auth_AS_User_Handler
from neurospeed.api_socket_handlers.downlink_room_as_user_handler import DownlinkRoom_AS_User_Handler
from neurospeed.utils.helper_service import UtilService




def downlink_message_external_handler(downlink_handler_instance, payload):
    username = downlink_handler_instance.get_username()
    print('Recieved downlink message from {}'.format(username))

    

def main():
    
    # load users configuration
    # user1_config_path = os.path.join(str(Path().absolute()) ,"config","hia_config1.json")
    config_user1 = UtilService.load_config_file('config/hia_config1.json')

    # create Auth_AS_User_Handler for each user and pass user configuration 
    user1_auth = Auth_AS_User_Handler(config_user1)
    user1_auth.login()

    
    # example connecting to SSR downlink and listen on events from customer
    user1_downlink = DownlinkRoom_AS_User_Handler(user1_auth)
    user1_downlink.set_downlink_router_external_handler(downlink_message_external_handler)
    user1_downlink.connect()
    
    # send message to all user machines connected to this downlink room except for the sender itself and the Customer
    time.sleep(2)
    if user1_downlink.is_connected():
       print('sending message to user machines')
       message = "Hello to every USER machine connected to this downlink room.\n" 
       user1_downlink.route_message(message)
    
    


if __name__ == '__main__':    
    main()  