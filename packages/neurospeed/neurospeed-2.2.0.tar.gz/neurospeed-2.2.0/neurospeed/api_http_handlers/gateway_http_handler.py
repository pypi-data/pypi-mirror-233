# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 20:12:14 2021

@author: NeuroBrave
"""

from neurospeed.utils.http_service import HttpService
import copy 
import json

class Gateway_HttpHandler:
    
    def __init__(self, customer_auth_handler):
        self._customer_auth  = customer_auth_handler
        self._http_service = HttpService()
        
        self._headers =  {
                "Authorization": "Bearer " + customer_auth_handler.get_access_token()
        }

    # returns list of connected users : 
    # [{id: number; username: string;}, ..., {id: number; username: string;}]
    def get_connected_users(self):
        endpoint = "/gateway/users/connected"
        params = {}
        response = self._http_service.GET_request(endpoint, params, self._headers)
        return response

    def get_connections(self, pager, filters): 
         endpoint = "/gateway/connections"
         request = json.dumps({"filters": filters, "pager": pager})
         headers_copy = copy.deepcopy(self._headers)
         headers_copy["content-type"] = "application/json"
         response = self._http_service.POST_request(endpoint, request, headers_copy)
         return response
     
        
