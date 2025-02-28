#------------------------------------------------------------------#
# SPG9000_Exporter.py                                              #
#                                                                  #
# Author:        Mike Kurras                                       #
# Date:          2/27/2025                                         #
# Description:   OpenMetrics exporter for Telestream SPG9000 Sync  #
#                Pulse Generator.                                  #
#                Designed for use with Prometheus                  #
#------------------------------------------------------------------#

import os
import requests
import datetime
import time
import json

from SPG9000_Formatter import format_reference_status
from SPG9000_Formatter import format_ptp_status
from SPG9000_Formatter import format_system_health
from SPG9000_Formatter import format_system_status

#------------------------------------------------------------------#
#Default Settings Overridden by ENV Variables
#------------------------------------------------------------------#
DEBUG = os.getenv('SPG9000_Exporter_Debug_Mode', False)

#Overridden at runtime
SPG9000_IP_ADDRESS = ''
API_KEY = ''

#Development Only
API_ROOT = '/api/v1.0'

#------------------------------------------------------------------#
#Settings for /System/Status
#------------------------------------------------------------------#
#Enable?
POLL_SYSTEM_STATUS = True
POLL_SYSTEM_STATUS_SCHEMA = f'/system/status'

#------------------------------------------------------------------#
#Settings for /System/Health
#------------------------------------------------------------------#
#Enable?
POLL_SYSTEM_HEALTH = True
POLL_SYSTEM_HEALTH_SCHEMA = f'/system/health'

#------------------------------------------------------------------#
#Settings for /Reference/Status
#------------------------------------------------------------------#
#Enable?
POLL_REFERENCE_STATUS = True
POLL_REFERENCE_STATUS_SCHEMA = f'/reference/status'


#------------------------------------------------------------------#
#Settings for /ptp/{instance}
#------------------------------------------------------------------#
POLL_PTP_STATUS = True
POLL_PTP_INSTANCES = "1,2"
POLL_PTP_STATUS_SCHEMA = f'/ptp'
POLL_PTP_STATUS_SCHEMA_BRANCHES = 'default-ds,parent-ds,port-ds-list'


#------------------------------------------------------------------#
#Logger Function
#------------------------------------------------------------------#
def debug(data):
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    if DEBUG:
        print(f'{timestamp}\t{data}')

#------------------------------------------------------------------#
#This method is the main API Call Skeleton
#------------------------------------------------------------------#
def api_get(schema):
    
    #Construct the Request URL
    request_url = f'http://{SPG9000_IP_ADDRESS}{API_ROOT}{schema}'
    
    debug(f'Sending Request to: {request_url}')
    
    #Set Headers
    headers = {
        "accept": "application/json",
        "X-API-Key": API_KEY
    }
    
    try:
        response = requests.get(request_url, headers=headers)
        response.raise_for_status()
        

        #Check for HTTP 200 OK Response
        if response.status_code == 200:
            #If HTTP 200 OK, then return response body
            debug("Response 200 OK!")
            debug("Parsing JSON...")
            
            try:
                json_response = json.loads(response.text)
                debug("JSON Data Successfully Parsed!")
                return json_response
            except Exception as e:
                debug(f'A JSON Parsing Error Occurred: {e}')
        
        #Otherwise Raise an Exception    
        else:
            raise()
    
    except requests.exceptions.RequestException as e:
        debug(f'An Error Occurred with HTTP Request: {e}')


#------------------------------------------------------------------#
#Helper for /System/Status
#------------------------------------------------------------------#
def poll_system_status():
    data = api_get(POLL_SYSTEM_STATUS_SCHEMA)
    prometheus_data = format_system_status(data)
    return prometheus_data

#------------------------------------------------------------------#
#Helper for /System/Health
#------------------------------------------------------------------#
def poll_system_health():
    data = api_get(POLL_SYSTEM_HEALTH_SCHEMA)
    prometheus_data = format_system_health(data)
    return prometheus_data

#------------------------------------------------------------------#
#Helper for /Reference/Status
#------------------------------------------------------------------#
def poll_reference_status():
    data = api_get(POLL_REFERENCE_STATUS_SCHEMA)
    prometheus_data = format_reference_status(data)
    return prometheus_data

#------------------------------------------------------------------#
#Helper for /ptp/{instance}
#------------------------------------------------------------------#
def poll_ptp_status():
    instances = POLL_PTP_INSTANCES.split(",")
    data = {}
    for instance in instances:
        branches = POLL_PTP_STATUS_SCHEMA_BRANCHES.split(",")
        branch_data = {}
        for branch in branches:
            branch_data.update({branch: api_get(f'{POLL_PTP_STATUS_SCHEMA}/{instance}/{branch}')})
        data.update({instance: branch_data})
    prometheus_data = format_ptp_status(data)
    
    return prometheus_data

#------------------------------------------------------------------#
#Main execution unit
#------------------------------------------------------------------#
def polldata (targetip, api_key):
    debug(f'Target: {targetip}')
    debug(f'API_KEY: {api_key}')
    
    #Override address and apikey key with runtime values
    global SPG9000_IP_ADDRESS
    SPG9000_IP_ADDRESS = targetip
    global API_KEY
    API_KEY = api_key
    
    data = []
    #Only run the subroutines enabled
    if POLL_SYSTEM_STATUS == True:
        data.append(poll_system_status())
    if POLL_SYSTEM_HEALTH == True:
        data.append(poll_system_health())
    if POLL_REFERENCE_STATUS == True:
        data.append(poll_reference_status())
    if POLL_PTP_STATUS == True:
        data.append(poll_ptp_status())
        
    full_data = "\n".join(data)
    return full_data