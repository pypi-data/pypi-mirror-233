# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 11:04:53 2021

@author: NeuroBrave
"""

from pathlib import Path
import os
from neurospeed.utils.helper_service import UtilService

from neurospeed.auth.auth_as_customer_handler import Auth_AS_Customer_handler
from neurospeed.api_http_handlers.gateway_http_handler import Gateway_HttpHandler 

global customer_auth

 
#### Gateway_HttpHandler.get_connections response: (TypeScript syntax)
#
# {
#    "pager": {
#        "total_records": number           # total records\entries found applying search filters
#        "total_pages": number             # total number of entries after applying search filters
#        "page_number": number             # requested page number
#        "page_size": number               # requested page number 
#        "actual_page_size": number        # it might be that acutal returned page size is smaller then requested. actual_page_size === items.length
#        "items": any[]                    # list of found items, (list of Connection_Dto objects in this case)
#     },
#   "filters": {}                          # applied filters
# }
#
################################# 
# Connection_Dto {
#    id: number;
#    username: string;
#    sensors: any[]
#    socket_id: string;
#    sensors_count: number
#    online: {hours: number, minutes: number}
#    hia_id: string;
#    is_connected: boolean;
#    connected_at: Date;
#    disconnected_at: Date;
#    updated_at: Date;
# }
####

def print_list_response(list_response): 
    pager = list_response["pager"]
    
    total_records = pager["total_records"] 
    total_pages = pager["total_pages"]
    page_number = pager["page_number"]
    page_size = pager["page_size"]    
    actual_page_size = pager["actual_page_size"]  
    items = pager["items"]
    
    filters = list_response["filters"]  

    
    print("HIA_CONNECTION - query with filters: {} results in {} entries and {} pages".format(filters, total_records, total_pages))
    print("HIA_CONNECTION - page_number: {} requested page_size: {} actual page_size: {} ".format(page_number, page_size, actual_page_size))
    
    for item in items:
        # custom
        pass


# Hint: you can set "Verbose_socket_log": "True" in customer config to enable more logging
def main():
    global customer_auth

    # load customer config file
    customer_config_path = os.path.join(str(Path().absolute()) ,"config","customer_config.json")
    customer_config = UtilService.load_config_file(customer_config_path)
    
    # Authenticate as customer
    customer_auth = Auth_AS_Customer_handler(customer_config)
    customer_auth.login()
    
    gateway = Gateway_HttpHandler(customer_auth)
    connected_users = gateway.get_connected_users()

    username_array = []
    for user in connected_users:
        username_array.append(user["username"])
        
    print('connected user array: {}'.format(username_array))
    
    # using get_connections() API call, you can query user HIA device connections
    # returns list of connection entries, already sorted where recent updated entires come first
    if len(username_array ) > 0:
        print('quering Neurospeed API for connected user device')

        page_number = 1 # required
        page_size = 50 # required. Max page size: 100
        
        pager = { # required
            "page_number": page_number,
            "page_size": page_size
        }
        filters = { # not required
            "is_connected": True, # if is_connected is not set or False, query would return both connected and disconnected entries
            "usernames": username_array, # array of usernames, if array is empty or not set, query would search for entires across all users
        }
        
        connected_connections_response = gateway.get_connections(pager, filters)
        print_list_response(connected_connections_response)
    else: 
        print('No connected users')

    # example query all connections (currently connected and disconnected) for all users:
    print('Quering Neurospeed API for all user device connections')   
    
    page_number = 1 
    page_size = 20 


    pager = {
        "page_number": page_number,
        "page_size": page_size
    }
    filters = {}
    
    all_connections_response = gateway.get_connections(pager, filters )
    print_list_response(all_connections_response)
   




if __name__ == '__main__':    
    main()  
    
    
    