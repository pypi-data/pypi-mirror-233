
'''

this script sends data from EEG raw recordings in CSV format to neurospeed, and downloads the processed output files
the scripts expects a /config subfolder with following files:
    dashboard_credentials.json - for customer-level auth (to operate the recorder-exporter function)
        inside:
            {
            "email": "",
            "password": ""
            }


    HIA_config.json - for user-level auth (to send the EEG data)
        inside:
            {
                "account_id": "neurobrave_Nt57tr0rSG",
                "username": "oleg@neurobrave",
                "user_password": "oleg123321",
            }
    optional: api_config.json (if exists, the neurospeed server address will be used from this file. useful for running on non-default neurospeed servers.)
        inside:

            {
            "is_prod": "True",
            "api_address_prod": "https://api-test.neurospeed.io",
            "api_address_local":  "http://localhost:3000",
        	"pipeline_address_prod": "wss://api-test.neurospeed.io",
        	"pipeline_address_local": "ws://localhost:3000",
            }

    the scripts expects a "raw_data_folder" subfolder in it's root location (current working directory)
    in that "raw_data_folder" subfolder expected to be separate folder for each subject's experiment.
    the list "tasks" defines in which order to send the datafiles to neurospeed, accoring to partial match of data file names
    to keyword in the list
    the script saves to the "raw_data_folder" an exported datafle downloaded from NeuroSpeed; with labels according to the keywords.

    the data files expected to be in formats:
        CSV comma separated file

        data columns:
        timestamps, EEG channel 0,..EEG channel N

        timestamps are discarded when sending data


'''
import json
import numpy as np
import os
import sys
import time
import logging
import requests
from datetime import datetime
import pandas as pd

from neurospeed.auth.auth_as_user_handler import Auth_AS_User_Handler
# from neurospeed.api_socket_handlers.downlink_room_as_user_handler import DownlinkRoom_AS_User_Handler
from neurospeed.utils.helper_service import UtilService
from neurospeed.hia_user_data.neurobrave_sensor_interface import HIA_Client

from neurospeed.auth.auth_as_customer_handler import Auth_AS_Customer_handler
# from neurospeed.api_http_handlers.recorder_http_handler import UserRoom_Recorder_Handler
# from neurospeed.api_http_handlers.exporter_http_handler import UserRoom_Recorder_Exporter_Handler


from neurospeed.macros import macros



def generate_sensor_info(config, hia_config):
    '''
    this functiuon generates sensor_info dictionary that is nesessary ot initialize the HIA client.
    the sensor info is tailored for single EEG according to config
    only LSL interface supported currently

    input:
        hia_config dictionary
    '''
    # generate SOME sensors stream ids
    sensor_info = dict()

    if "EEG" in config["DATA_SOURCE"]:
        user_data_stream_id = "EEG" + '_' + UtilService.generateId(6)
        sensor_info[user_data_stream_id] = {
            "device_type": "EEG",
            "channel_count": len(hia_config["EEG_channel_enable"]),
            "sampling_frequency": hia_config["EEG_sample_rate"],
            "buffer_length": hia_config["EEG_buffer_length_seconds"],
            "manufacturer_id": "NeuroBrave",
            "sensor_id": user_data_stream_id,
            "stream_id": user_data_stream_id,
            "stream_state": "enabled",
            "channel_map": hia_config["channel_map"]
        }

    if "PPG" in config["DATA_SOURCE"]:
        user_data_stream_id = "PPG" + '_' + UtilService.generateId(6)
        sensor_info[user_data_stream_id] = {
            "device_type": "PPG",
            "channel_count": len(hia_config["PPG_channel_map"]),
            "sampling_frequency": hia_config["PPG_sample_rate"],
            "buffer_length": hia_config["PPG_buffer_length_seconds"],
            "manufacturer_id": "NeuroBrave",
            "sensor_id": user_data_stream_id,
            "stream_id": user_data_stream_id,
            "stream_state": "enabled",
            "channel_map": hia_config["PPG_channel_map"]
        }

    if "SMARTWATCH" in config["DATA_SOURCE"]:
        user_data_stream_id = "PPG" + '_' + UtilService.generateId(6)
        sensor_info[user_data_stream_id] = {
            "device_type": "SMARTWATCH",
            "channel_count": len(hia_config["PPG_channel_map"]),
            "sampling_frequency": hia_config["PPG_sample_rate"],
            "buffer_length": hia_config["PPG_buffer_length_seconds"],
            "manufacturer_id": "NeuroBrave",
            "sensor_id": user_data_stream_id,
            "stream_id": user_data_stream_id,
            "stream_state": "enabled",
            "channel_map": hia_config["PPG_channel_map"]
        }


    if "GSR" in config["DATA_SOURCE"]:
        for idx, port in enumerate(config["OPENBCI_COM_PORT"]):
            user_data_stream_id = "GSR" + '_' + UtilService.generateId(6)
            sensor_info[user_data_stream_id] = {"device_type": "GSR",
                                                "sensor_id": user_data_stream_id,
                                                "stream_id": user_data_stream_id,
                                                "sampling_frequency": 250,
                                                "buffer_length": 1.0,
                                                "manufacturer_id": "openBCI",
                                                "channel_count": len(config["GSR_channel_enable"][idx]),
                                                # "Downstream ID":downstream_id,
                                                "channel_map": config["GSR_channel_map"][idx],
                                                "stream_state": "enabled"}

    if "EDA" in config["DATA_SOURCE"]:
        user_data_stream_id = "GSR_ADIEDA"

        sensor_info[user_data_stream_id] = {"device_type": "GSR",
                                            "sensor_id": user_data_stream_id,
                                            "stream_id": user_data_stream_id,
                                            "sampling_frequency": config["EDA_sampling_frequency"],
                                            "buffer_length": 1.0,
                                            "manufacturer_id": "ADI",
                                            "channel_count": 6,
                                            # "Downstream ID":downstream_id,
                                            "channel_map": ['real', 'img', 'adm_real', 'adm_img', 'adm_mag',
                                                            'adm_phase', "timestamp"],
                                            "stream_state": "enabled"}
    return sensor_info


def disconnect_external_handler(hia_client):
    # logging.debug("hia:["+ hia_client.get_hia_id()+"]"+ "user:["+ hia_client.get_username()+"] disconnected ")
    pass


# would be called for each hia after successfuly connection
def connection_external_handler(hia_client):
    pass
    # logging.debug('connected as '+ hia_client.get_username()+ " with hia: " +hia_client.get_hia_id()+ ". sending data..")


def init_HIA_client(config, hia_config):
    '''
    this functiuon  initialize the HIA client and connect the cloud streaming (upload raw data to neurospeed)
    the sensor info is tailored for single EEG according to config
    only LSL interface supported currently

    input:
        config - dictionary with config for this epxeriment program
        hia_config dictionary

    output
        hia_user client object instance
        sensor info dictionary

    '''
    user1_auth = Auth_AS_User_Handler(hia_config)
    user1_auth.login()

    hia_sensor_info_user1 = generate_sensor_info(config, hia_config)

    logging.debug('Generated sensor info: {}'.format(hia_sensor_info_user1))
    hia_user1 = HIA_Client(user1_auth, hia_sensor_info_user1)
    hia_user1.set_socket_connection_external_handler(connection_external_handler)
    hia_user1.set_socket_disconnect_external_handler(disconnect_external_handler)
    logging.debug("HIA_ID: " + str(user1_auth.get_hia_id()))
    hia_user1._device_type = "PPG"
    hia_user1.connect()
    return hia_user1, hia_sensor_info_user1



def send_EEG_to_websocket_from_files_in_datafolder(datafolder, hia_client, hia_sensor_info_user1, hia_config,
                                                   datatypes=["EEG"]):
    df_exporter = None
    for item in os.listdir(datafolder):
        if "_exported" in item and ".csv" in item:
            path = os.path.join(datafolder, item)
            df_exporter = pd.read_csv(path, delimiter=",", usecols=[
                'timestamp', 'exp.0', 'input.TP9', 'input.AF7', 'input.AF8', 'input.TP10', 'stream_id'
            ])
            break
    if df_exporter is None:
        raise ValueError("no Exporter file found!!!")
        # stream = df_exporter["stream_id"].unique()[0]
    print(df_exporter['stream_id'].dropna().unique())
    src_stream = [stream_id for stream_id in df_exporter['stream_id'].dropna().unique() if 'EEG_' in stream_id][-1]
    stream = list(filter(lambda x: x.startswith(datatypes[-1]), list(hia_sensor_info_user1.keys())))[0]

    df_eda = df_exporter.query(f"stream_id == @src_stream")
    eeg_labels_array = df_eda["exp.0"].to_numpy()
    data_array = df_eda.drop(columns=['timestamp', 'exp.0', 'stream_id']).to_numpy()

    stream_id = stream
    old_key = list(hia_sensor_info_user1.keys())[-1]
    hia_sensor_info_user1[stream] = hia_sensor_info_user1.pop(old_key)
    window = 256
    read_index = 0
    current_label = None
    print(f"length of data: {len(data_array)}")
    print(f"shape of the array is {data_array.shape}")
    while read_index + window < len(data_array):
        data = data_array[read_index:read_index + window].tolist()
        read_index += window
        hia_client.send_data_direct(data, stream_id, send_without_timestamp=True, device_type="EEG")
        print("tranmsmitting data packet")
        time.sleep(0.1)
        if data_array[read_index] != current_label:
            hia_client.set_label(eeg_labels_array[read_index])
            current_label = eeg_labels_array[read_index]
            print(f"setting label to {current_label}")


if __name__ == '__main__':




    config = {}
    config["DATA_SOURCE"] = ["EEG"]
    config["patientname"] = "olegtest"


    #put here a path to folder that has a CSV file in neurospeed format, that has "exported" in it's name: 
    datafolder = "H:\\DATASETS\\Simon-Waldo-Prime-Fix-Relax\\Experiment Recording\\Test\\data"

    hia_client = None
    with open('config/hia_config.json') as f:
        hia_config = json.load(f)

    with open('config/dashboard_credentials.json') as f:
        customer_config = json.load(f)
    # Authenticate as customer on neurospeed.io:
    customer_auth = Auth_AS_Customer_handler(customer_config)
    customer_auth.login()


    recorder_id = macros.start_recording(customer_auth, hia_config, recorder_name=config["patientname"])

    max_hia_reconnect_retries = 3
    for reconnect_idx in range(max_hia_reconnect_retries):
        hia_client, hia_sensor_info = init_HIA_client(config, hia_config)
        if hia_client.is_connected():
            break
        else:
            logging.debug("HIA connection retrying...")
            time.sleep(3)

    if not hia_client.is_connected():
        print("FAILED connecting to cloud streaming!\n")
        sys.exit()


   
    if 'EEG' in config["DATA_SOURCE"]:
        send_EEG_to_websocket_from_files_in_datafolder(datafolder, hia_client, hia_sensor_info,
                                                       hia_config,
                                                       config["DATA_SOURCE"])

    hia_client.disconnect()
    print("hia status: " + str(hia_client.is_connected()))
    macros.stop_recording(recorder_id)

    exporter_config = {
        "custom_name": config["patientname"] + "_exported",
        "start_timestamp_mode": "start",
        "end_timestamp_mode": "end"
    }
    save_folder = os.path.join(os.getcwd(), datafolder)
    exporter_filename = macros.download_data(customer_auth, recorder_id, exporter_config, hia_config,
                                             save_folder)
