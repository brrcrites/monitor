import subprocess
import re
import requests
import json
import argparse

from proc_info import ProcInfo
from logs import LogInfo

def parse_config_json(config_location):
    try:
        fd = open(config_location,'r')
        file_str = fd.read()
    except:
        print('The config file located at "%s" failed to open or read' % config_location)
        exit(-1) # TODO: raise an exception here instead
    try:
        file_json = json.loads(file_str)
    except:
        print('The config file located at "%s" failed to parse as valid JSON' % config_location)
        exit(-1) # TODO: raise an exception here instead
    return file_json

parser = argparse.ArgumentParser(description = 'Client for sending monitoring data to central server')
parser.add_argument('--config', type=str, help='Path to the JSON configuration file [required]', required=True)
args = parser.parse_args()

config = parse_config_json(args.config)

info = ProcInfo(config)
print(info.get_num_proc())
print(info.get_utilization())

logs = LogInfo(config)
print(logs.get_log_file())
