# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 12:37:54 2021

@author: NeuroBrave
"""

from neurospeed.utils.http_service import HttpService

class Auth_AS_Customer_handler:

    def __init__(self, customer_config):
        self._contex = "Auth_As_Customer_Handler - "
        self._customer_config = customer_config
        self._access_token = None
        self._customer_email = self._customer_config["email"]
        self._auth_api_instance = self.Customer_Auth_Api(self)

        

    # login as customer
    def login(self):
        try:
            self._login_status = self._auth_api_instance.customer_login()
            if self._login_status == True:
                self._access_token = self._auth_api_instance.get_access_token()
                print('{} Successful login as customer {}'.format(self._contex, self._customer_email) )
            else:
               raise ValueError()
        except:
               print('{} Unable to login as [{}]'.format(self._contex, self._customer_email) )
               self._login_status = False
            
        finally:
            return self._login_status

        
    def get_access_token(self):
        return self._access_token
    
    def get_config(self):
        return self._customer_config

    def get_customer_email(self):
        return self._customer_email
    
    def is_logged_in(self):
        return self._login_status
    
    def get_hia_id(self):
        return self._customer_config["HIA_ID"]

    def is_verbose_log(self):
        return self._customer_config["Verbose_socket_log"] == "True"
 
    
    class Customer_Auth_Api:
        
        def __init__(self, auth_handler_instance):
            self._contex = "Customer_Auth_Api - "
            
            self._customer_config = auth_handler_instance.get_config()
            self._customer_email = self._customer_config["email"]
            self._customer_password  = self._customer_config["password"]
 
            self._http_service = HttpService()
            
        # login api flow
        def customer_login(self):
            endpoint = "/auth/login"
            
            print("{} Executing login flow as customer [{}]".format(self._contex, self._customer_email))
            
            login_payload = {
                "email": self._customer_email, 
                "password": self._customer_password,
            }
            login_status = False
            try:
                response_payload =  self._http_service.POST_request(endpoint, login_payload)
                
                token = response_payload["token"]
                self._access_token = token["accessToken"]
                # print("Customer access_token: ", self._access_token)
                login_status = True
            
            except:
                   raise ValueError() 

      
            return login_status
    
            
        def get_access_token(self):
            return self._access_token
