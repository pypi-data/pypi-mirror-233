# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 12:37:54 2021

@author: NeuroBrave
"""


from neurospeed.utils.http_service import HttpService

class Auth_AS_User_Handler:

    def __init__(self, user_config):
        self._contex = "User_Auth_Handler - "
        self._user_config = user_config
        self._user_username = self._user_config["username"]
        self._access_token = None
        self._login_status = None
        self._account_id = None
        self._auth_api_instance = self.User_Auth_Api(self) # 
    

    
    # login as HIA user
    def login(self):
        try:
            self._login_status = self._auth_api_instance.user_login()
            if (self._login_status == True):
                self._access_token = self._auth_api_instance.get_access_token()
                print('{} successful user login as {}'.format(self._contex, self._user_username) )
            else:
               raise ValueError()
        except:
            print('{} Unable to login as {}'.format(self._contex, self._user_username))
            self._login_status = False
            
        finally:
            return self._login_status
        
    def get_access_token(self):
        return self._access_token
    
    def get_config(self):
        return self._user_config
    
    def get_hia_id(self):
        return self._user_config["HIA_ID"]
    
    def get_username(self):
        return self._user_config["username"]
    
    def is_logged_in(self):
        return self._login_status
    
    def is_verbose_log(self):
        return self._user_config["Verbose_socket_log"] == "True"

    class User_Auth_Api:
    
        def __init__(self, auth_handler_instance):
            self._contex = "User_Auth_Api -"
            
            self._user_config = auth_handler_instance.get_config()
            if "account_id" in self._user_config:                
                self._account_id  = self._user_config["account_id"] 
            else:
                self._account_id  = self._user_config["customer_username"] 
                
            self._user_username  = self._user_config["username"]
            self._user_password  = self._user_config["user_password"]

            self._http_service = HttpService()
             
             
        def user_login(self):
            endpoint = "/users/login"
        
            print("{} Executing Login as User {}".format(self._contex, self._user_username))

            login_payload = {
                "account_id": self._account_id, 
                "username": self._user_username, 
                "password": self._user_password,
            }
            login_status = False
            try:
                response_payload =  self._http_service.POST_request(endpoint, login_payload)
                
                token = response_payload["token"]
                self._access_token = token["accessToken"]
                # print("User access_token: ", self._access_token)
                login_status = True
            
            except:
                   raise ValueError() 
            
            return login_status
            
        
        def get_access_token(self):
            return self._access_token
        