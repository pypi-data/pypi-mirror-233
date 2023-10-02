

from neurospeed.utils.helper_service import UtilService as utils
from pathlib import Path
import os

class ApiConfig:

    def __init__(self):
        self._contex = "ApiConfig - "
        
        '''
        precedence of config path options: 
        
        if C:/neurobrave/hia_config.json exists, it's used
        otherwise, if /config/api_config.json exists under the runtime folder, its' used
        it none of these exist, defauilt that comes with the neurospeed library is used.
            
        '''
        # if os.path.isfile("C://neurobrave//HIA_config.json"):
        #     self._config_path = "C://neurobrave//HIA_config.json"
        #     print("using HIA config for API URL")
        # elif os.path.isfile(os.path.join(os.getcwd(),"config", "api_config.json")):
        #     self._config_path = os.path.join(os.getcwd(),"config", "api_config.json")
        #     print("using program config for API URL")
        # else:     
        #     self._config_path =  os.path.join(str(Path(__file__).parent.parent) ,"config","api_config.json")

        if os.path.isfile(os.path.join(os.getcwd(),"config", "api_config.json")):
            self._config_path = os.path.join(os.getcwd(),"config", "api_config.json")
            print("using program config for API URL")
        else:     
            self._config_path =  os.path.join(str(Path(__file__).parent.parent) ,"config","api_config.json")


        self._api_config = utils.load_config_file(self._config_path)
        self._api_http_url =  self._api_config["api_address_prod"]  if self._api_config["is_prod"] == "True"  else  self._api_config["api_address_local"] 
        self._pipeline_url =  self._api_config["pipeline_address_prod"]  if self._api_config["is_prod"] == "True"  else  self._api_config["pipeline_address_local"] 
        print("api config path: " + self._config_path)
        print("{} NeuroSpeed API HTTP URL: {} ".format(self._contex, self._api_http_url))
        print("{} NeuroSpeed API SOCKET URL: {} ".format(self._contex, self._pipeline_url))
        
    def get_http_url(self):
        return self._api_http_url
    
    def get_socket_url(self):
        return self._pipeline_url
        