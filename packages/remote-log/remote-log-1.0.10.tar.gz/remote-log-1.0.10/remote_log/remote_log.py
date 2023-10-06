import requests
import os
import json
from .sysinfo import get_system_info

# Base directory for the library
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OFFLINE_LOGS_DIR = os.path.join(BASE_DIR, "offline_logs")

# Ensure the offline_logs directory exists
if not os.path.exists(OFFLINE_LOGS_DIR):
    os.makedirs(OFFLINE_LOGS_DIR)

def get_offline_storage_path(url):
    # Convert the URL to a filename-friendly string
    filename = ''.join(e for e in url if e.isalnum())
    return os.path.join(OFFLINE_LOGS_DIR, f"{filename}_offline_payloads.json")

def send_data(url, payload, offline_storage_path):
    # Try to send the payload
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Clear the offline storage file after sending
        if os.path.exists(offline_storage_path):
            os.remove(offline_storage_path)
    
    except requests.RequestException:
        # If the request fails, store the current payload for later
        new_payload = {
            "log": payload["data"][0]["log"],
            "system": get_system_info()
        }
        
        if os.path.exists(offline_storage_path):
            with open(offline_storage_path, 'r') as file:
                offline_payloads = json.load(file)
            # Insert the new payload at the beginning (stack-like order)
            offline_payloads.insert(0, new_payload)
        else:
            offline_payloads = [new_payload]
        
        with open(offline_storage_path, 'w') as file:
            json.dump(offline_payloads, file)

def remote_log(url, log):
    # Define the payload for the POST request
    payload = {
        "data": [
            {
                "log": log,
                "system": get_system_info()
            }
        ]
    }
    
    # Get the offline storage path for the given URL
    offline_storage_path = get_offline_storage_path(url)
    
    # Check for previously stored payloads and add them to the data
    if os.path.exists(offline_storage_path):
        with open(offline_storage_path, 'r') as file:
            offline_payloads = json.load(file)
        payload["data"].extend(offline_payloads)
    
    send_data(url, payload, offline_storage_path)

# Example usage:
# url = "http://example.com/api"
# command = "some_command"
# remote_log(url, command)
